import argparse
import os
import subprocess
import sys
import csv

def create_output_folder(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def get_java_lines(repo_path, commit_hash):
    try:
        os.chdir(repo_path)
        command = f'git show --pretty="format:" --name-only {commit_hash}'

        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            file_list = result.stdout.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")
            return None

        java_lines_count = 0

        for file in file_list:
            if file.endswith('.java'):
                file_path = os.path.join(repo_path, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as java_file:
                        lines_count = sum(1 for line in java_file)
                except FileNotFoundError:
                    lines_count = 100
                except Exception as ex:
                    print(f"Error processing file {file}: {ex}")
                    lines_count = 100
                java_lines_count += lines_count

        return java_lines_count

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def add_to_retry_csv(commit_hash, retry_csv_path):

    if not os.path.exists(retry_csv_path):
        with open(retry_csv_path, 'w', newline='') as csvfile:
            fieldnames = ["commit"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(retry_csv_path, 'a', newline='') as csvfile:
        fieldnames = ["commit"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"commit": commit_hash})

def analyze_commit_and_save(repository_path, output_path, all_commit_analyzing_branch_name, current_commit, csv_file_path):

    retry_count = 0
    retry_csv_path="retry.csv"
    commit_to_retry = None

    while retry_count < 3:
        try:
            if commit_to_retry:
                # print(f"Last un-successfully analyzed commit: {commit_to_retry}")
                current_commit =commit_to_retry
            designite_command = f"java -jar DesigniteJava.jar -i {repository_path} -o {output_path} -aco {all_commit_analyzing_branch_name} -fr {current_commit}"
            subprocess.run(designite_command, check=True)
            
            break 

        except subprocess.CalledProcessError as e:
            retry_count += 1

            if retry_count < 3:
                print(f"Retrying ({retry_count}/3)...")
                commit_to_retry = print_commit_after_error(output_path)
                continue
            else:
                update_csv_with_output_folder(output_path, csv_file_path)
                add_to_retry_csv(commit_to_retry, retry_csv_path)
                print(f"Failed to analyze commit {current_commit} after 3 attempts. Moving to next commit.")
                commit_to_retry = get_next_commit(repository_path, current_commit)
                # print(f"next commit is ---------------------{commit_to_retry}")
                return commit_to_retry

def print_commit_after_error(output_path):
    log_files = [f for f in os.listdir(output_path) if f.startswith("DesigniteLog")]
    if not log_files:
        print("No DesigniteLog files found.")
        return None

    latest_log_file = max(log_files, key=lambda f: os.path.getctime(os.path.join(output_path, f)))
    log_file_path = os.path.join(output_path, latest_log_file)

    try:
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if "Analyzing commit" in line:
                    commit_hash = line.split()[-1]
                  
                    return commit_hash
    except Exception as ex:
        print(f"Error reading DesigniteLog file: {ex}")
        return None

def get_starting_commit(repository_path):
    try:
        starting_commit = subprocess.check_output(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=repository_path,
            text=True
        ).strip()
        return starting_commit
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting starting commit: {e}")
        sys.exit(1)

def get_next_commit(repository_path, current_commit):
    try:
        if current_commit is None:
            log_output = subprocess.check_output(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                cwd=repository_path,
                text=True
            ).strip()
        else:
            log_output = subprocess.check_output(
                ["git", "log", "--pretty=format:%H", "--reverse", f"{current_commit}..HEAD"],
                cwd=repository_path,
                text=True
            ).splitlines()

            if not log_output:
                return None
            log_output = log_output[0]
        return log_output
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting next commit: {e}")
        sys.exit(1)

def update_csv_with_output_folder(output_path, csv_file_path):
    existing_commits = set()

    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_commits.update(row["commit"] for row in reader)

    for commit_folder in os.listdir(output_path):
        commit_path = os.path.join(output_path, commit_folder)
        if os.path.isdir(commit_path):
            commit_hash = commit_folder
            if commit_hash not in existing_commits:
                with open(csv_file_path, 'a', newline='') as csvfile:
                    fieldnames = ["commit"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({"commit": commit_hash})
                existing_commits.add(commit_hash)

def add_commit_to_csv(commit_hash, csv_file_path):
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_commits = {row["commit"] for row in reader}

    if commit_hash not in existing_commits:
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ["commit"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({"commit": commit_hash})

def run_designite_for_commits(repository_path, output_path, commit_sequence, csv_file_path):
    retry_count = 0

    for commit_list in commit_sequence:
        start_commit = commit_list[0]
        end_commit = commit_list[-1]

        retry_count = 0
        retry_csv_path="retry.csv"
        commit_to_retry = None
        while retry_count < 3:
            try:
                if commit_to_retry:
                    start_commit =commit_to_retry
                designite_command = f"java -jar DesigniteJava.jar -i {repository_path} -o {output_path} -aco {args.branch} -fr {start_commit} -to {end_commit}"
                subprocess.run(designite_command, check=True)
                update_csv_with_output_folder(output_path, csv_file_path)
                break
            except subprocess.CalledProcessError as e:
                retry_count += 1
                print(f"Error running Designite for commits {start_commit} to {end_commit}: {e}")
                if retry_count < 3:
                    print(f"Retrying ({retry_count}/3)...")
                    commit_to_retry = print_commit_after_error(output_path)
                    continue
                else:
                    update_csv_with_output_folder(output_path, csv_file_path)
                    add_to_retry_csv(commit_to_retry, retry_csv_path)
                    print(f"Failed to analyze commits {start_commit} to {end_commit} after 3 attempts.")
                    break

def remove_commits_incsv_not_in_output_folder(output_path, csv_file_path):
    output_commits = [commit_folder for commit_folder in os.listdir(output_path) if os.path.isdir(os.path.join(output_path, commit_folder))]

    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_commits = {row["commit"] for row in reader}

    commits_to_remove = existing_commits - set(output_commits)

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["commit"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for commit in existing_commits - commits_to_remove:
            writer.writerow({"commit": commit})

def remove_commits_incsv_empty_in_output_folder(output_path, csv_file_path):
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_commits = {row["commit"] for row in reader}

    for commit_folder in os.listdir(output_path):
        commit_path = os.path.join(output_path, commit_folder)

        if os.path.isdir(commit_path) and not os.listdir(commit_path):
            commit_hash = commit_folder

            if commit_hash in csv_commits:
                csv_commits.remove(commit_hash)

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["commit"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for commit_hash in csv_commits:
            writer.writerow({"commit": commit_hash})

def is_csv_empty(folder_path, commit):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        try:
            with open(csv_file_path, 'r') as file:
                content = file.read().strip()

                if content and not all(line.strip() == "" or line.isspace() for line in content.split('\n')[1:]):
                    return False
        except Exception as e:
            print(f"Error reading CSV file {csv_file} in commit {commit}: {e}")
    return True

def remove_commits_incsv_emptyHeaders_and_notZeroLOC(output_path, csv_file_path, repo_path):
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_commits = {row["commit"] for row in reader}

    for commit_folder in os.listdir(output_path):
        commit_path = os.path.join(output_path, commit_folder)

        if os.path.isdir(commit_path) and os.listdir(commit_path):
            commit_hash = commit_folder
            current_dir = os.getcwd() 
            lines_count = get_java_lines(repo_path, commit_hash)
            os.chdir(current_dir) 
            if lines_count is not None and lines_count > 0:
            
                if commit_hash in csv_commits and is_csv_empty(commit_path, commit_hash):
                    csv_commits.remove(commit_hash)
                    # print(f"Commit {commit_hash} removed from CSV file as it has non-zero LOC and not empty CSV.")
                # print(f"Java LOC for commit {commit_hash}: {lines_count}")
                    
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["commit"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for commit_hash in csv_commits:
            writer.writerow({"commit": commit_hash})

def remove_commits_in_retry_csv(unanalyzed_commits, retry_csv_path):
 
    if os.path.exists(retry_csv_path):
        with open(retry_csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            retry_commits = {row["commit"] for row in reader}

        unanalyzed_commits = [commit_hash for commit_hash in unanalyzed_commits if commit_hash not in retry_commits]

    return unanalyzed_commits

def sort_commits_by_sequence(unanalyzed_commits, sequential_commits_list):
    commit_indices = {commit: index for index, commit in enumerate(sequential_commits_list)}
    sorted_commits = sorted(unanalyzed_commits, key=lambda commit: commit_indices.get(commit, float('inf')))

    return sorted_commits

def get_continuous_commits(repository_path, branch="main"):
    try:
        git_log_command = ["git", "log", "--pretty=format:%H","--reverse", f"{branch}"]
        commit_hashes = subprocess.check_output(git_log_command, cwd=repository_path, text=True).strip().split('\n')
        return commit_hashes
    
    except subprocess.CalledProcessError as e:
        print(f"Error fetching commits for the main branch: {e}")
        sys.exit(1)

def find_continuous_sequences(sequential_commits_list, unanalyzed_commits):
    result = []
    current_sequence = []

    for commit in unanalyzed_commits:
        if not current_sequence or sequential_commits_list.index(commit) == sequential_commits_list.index(current_sequence[-1]) + 1:
            current_sequence.append(commit)
        else:
            result.append(current_sequence)
            current_sequence = [commit]

    if current_sequence:
        result.append(current_sequence)
    if not result:
        print(f'All commits are analyzed!')
    # print(f'{result}')

    return result

def run_designite_with_output(repository_path, output_path, all_commit_analyzing_branch_name="main"):
    csv_file_path = os.path.join("", "analyzed_commits.csv")
    
    if not os.path.exists(output_path):
        print(f"Error: Output folder not present. Please create output folder for the provided path.")
        sys.exit(1)
    else:
        csv_file_path = os.path.join("", "analyzed_commits.csv")

    if not os.path.exists(csv_file_path):
        print(f"Error: Output folder has some analyzed commits, and CSV file '{csv_file_path}' not found. Try to run again from the first commit or make the output folder empty.")
        sys.exit(1)

    remove_commits_incsv_not_in_output_folder(output_path, csv_file_path)
    remove_commits_incsv_empty_in_output_folder(output_path, csv_file_path)
    remove_commits_incsv_emptyHeaders_and_notZeroLOC(output_path,csv_file_path,repository_path)
 
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_commits = {row["commit"] for row in reader}

    # Print existing commits
    # print("Existing commits in analyzed_commits.csv:")
    # for commit in existing_commits:
    #     print(commit)

    # Iterate over all commits in the Git repository
    # print("Commits not in analyzed_commits.csv:")
    try:
        all_commits = subprocess.check_output(
            ["git", "log", "--pretty=format:%H"],
            cwd=repository_path,
            text=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error getting all commits: {e}")
        sys.exit(1)

    unanalyzed_commits = [commit_hash for commit_hash in all_commits if commit_hash not in existing_commits]

    # for commit_hash in unanalyzed_commits:
    #     print(commit_hash)

    sequential_commits_list=get_continuous_commits(repository_path)
    unanalyzed_commits=sort_commits_by_sequence(unanalyzed_commits,sequential_commits_list)
    unanalyzed_commits = remove_commits_in_retry_csv(unanalyzed_commits, 'retry.csv')
    result=find_continuous_sequences(sequential_commits_list,unanalyzed_commits)
    
    run_designite_for_commits(repository_path, output_path, result, csv_file_path)

def run_designite_without_output(repository_path, all_commit_analyzing_branch_name="main",output_path="output"):
    if output_path:
        output_path = output_path
    else:
        output_path='output' 

    csv_file_path = "analyzed_commits.csv"
    
    if os.path.exists(output_path) and os.listdir(args.output):
        print(f"Error: Output folder '{output_path}' already exists. This repository already has some analyzed commits.")
        sys.exit(1)
    
    create_output_folder(output_path)

    starting_commit = get_starting_commit(repository_path)
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["commit"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    current_commit = starting_commit
    while current_commit:
        current_commit=analyze_commit_and_save(repository_path, output_path, all_commit_analyzing_branch_name, current_commit, csv_file_path)

    update_csv_with_output_folder(output_path, csv_file_path)

    print(f"Designite processing completed for all commits. Output saved to: {output_path}")
    print(f"Analyzed commits saved to: {csv_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Designite for a Git repository.")
    parser.add_argument("-i", "--repository", required=True, help="Local repository path")
    parser.add_argument("-o", "--output", default=None, help="Output path")
    parser.add_argument("-aco", "--branch", default="main", help="Branch name for analyzing all commits")

    args = parser.parse_args()

    if os.listdir(args.output) and args.output:
        run_designite_with_output(args.repository, args.output, args.branch)
    else:
        run_designite_without_output(args.repository, args.branch,args.output)


