# Designite util
The ```postprocessor``` script reads the output generated by DesigniteJava tool
and emits the output indexed by filepath.
```
Filepath, smell, project, package, type, method, cause, start_line_no
```

The ```designite_diff``` script computes the *diff* (in terms of detected smells) between two output folders generated by DesigniteJava.

## Usage
**post processor**

Run ```process``` function in ```postprocessor.py``` with a folder path where files generated from Designite are placed.

**designite_diff**

Run ```process``` function in ```designite_diff.py```. The script accepts two folder paths and assumes that both the folders are generated by DesigniteJava. The script returns the following output parameters.
- 1 : whether both the folders are same from detected smells perspective
- 2 and 3: list of different arch smells in folder 1 and 2 respectively
- 4 and 5: list of different design smells in folder 1 and 2 respectively
- 6 and 7: list of different impl smells in folder 1 and 2 respectively
