# homework-template-generator

A script to generate LaTeX files for homework. I recommend doing the following:
- Populate `courses.py` with the courses you're taking
- In your `.zshrc` file, add the following two lines:
```
export LATEX_GENERATOR_SCRIPT_PATH=/full/path/to/create_hw.py
alias genlatex="python $LATEX_GENERATOR_SCRIPT_PATH"
```
- Then, if you want to see which courses are listed, run `genlatex list <?Semester>` to list the courses (optionally for only a selected semester)
- When you're ready to create a new homework, create a directory for this homework, and from this dir, run:
```
genlatex "<COURSE_ID>" <Problem Set Number> <Due Date and Time> "<Collaborators>"
```
