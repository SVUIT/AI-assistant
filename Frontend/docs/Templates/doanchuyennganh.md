---
layout: default
title: Specialized project
parent: Templates
---

## Template templates

The template is built based on [sonnh-uit/HCMUIT_thesistemplate](https://github.com/sonnh-uit/HCMUIT_thesistemplate/tree/master)

### LaTeX template on OverLeaf

[Access](https://link.svuit.org/dacn-overleaf){: .btn .btn-primary }

### LaTeX template source code

[Access](https://github.com/SVUIT/report-templates/tree/main/specialized-project){: .btn .btn-primary }

## Instructions for using the subject project template

### Basic syntax

For those who have not used LaTeX or rarely use it, you can refer to the link [Instructions on OverLeaf](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes) to learn how to use basic syntax.

### File organization

```md
├── chapters
│ ├── front // Acronyms and Acknowledgements
│ | ├── glossaries.tex
│ | ├── thanks.tex
│ ├── main // Main content
│ | ├── chapter-1.tex
│ | ├── chapter-2.tex
│ | ├── conclusion.tex
│ | ├── intro.tex
│ | ├── summary.tex
├── graphics // Folder containing images
│ ├── chapter-1
│ | ├──pic-1.png
│ ├── chapter-2
│ | ├── pic-2.png
├── main.tex // Main file to aggregate content from other files
├── project.cls // Defines the cover page and some important formats such as margins, page frames.
├──ref.bib // Contains references at the end of the report
```

### Overleaf is better

The free version of OverLeaf will have certain limitations such as only allowing a maximum of 2 editors. Students of the Networking faculty can use [latex.uitiot.vn](https://latex.uitiot.vn/project) (log in with school email) to use premium features without additional fees, however it will be a bit slow when compiling.