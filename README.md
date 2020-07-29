# Homework and Paper Template Generator

A script to generate LaTeX files for homework and papers. I recommend doing the following:
- If you want to use the course feature, populate `courses.py` with the courses you're taking
- In your `.zshrc` file, add the following two lines:
```
export LATEX_GENERATOR_SCRIPT_PATH=/full/path/to/create_hw.py
alias genlatex="python $LATEX_GENERATOR_SCRIPT_PATH"
```
- Then, if you want to see which courses are listed, run `genlatex --list [--semester "<Semester>"]` to list the courses (optionally for only a selected semester)
- When you're ready to create a new homework, create a directory for this homework, and from this dir, run:
```
genlatex --generate-hw --course-id "<COURSE_ID>" --pset-number <Problem Set Number> --due-date <Due Date and Time> --collaborators "<?Collaborators>"
```
- When you want to create a new paper, create a directory for this paper, and
  from this dir, run:
```
genlatex --generate-paper --title "<PAPER TITLE>"
```
