## Introduction
myBiC is a web application for presenting analysis deliverables from the CHOP Bioinformatics Core to researchers. myBiC uses Django to handle Active Directory authentication and navigation.

Most projects will consist of a single index page (`index.html` or `index.md`) and links to several `static` files. 

Static files are those that are not parsed by the Django template engine, such as data files, pdfs, images, and stylesheets.

Both the index page and the static content should reside on the Isilon. There are management scripts within myBiC which manage symlinks to that content. The mount is read-only.

## The myBiC workflow
1. Create a repo in Github for your project
2. Create a directory on the Isilon for your large project deliverables
3. Create the index.md file in Github (recommended) or on the Isilon, can also be HTML if necessary
4. Edit myBiC Users/Groups/Labs as needed
5. Create a project in myBiC

## Understanding the authentication system
myBiC uses dirt simple users/groups authentication system but it can accomodate private projects, public projects, and projects accessible by members of more than one lab.

* `Labs` belong to a single `Group`. Labs are generally created at the same time as Groups in the Group admin http://mybic.chop.edu/admin/auth/group/
* `Projects` belong to a single `Lab`.
*  `Users` can belong to multiple `Groups`. 

Below is the Wallace group. Members of the Wallace group can see projects in both the Pei and Wallace labs.
![](https://dl.dropboxusercontent.com/u/4055239/modify_a_group.png)
If we wanted to create projects that only members of the Pei lab could see, we would have to create another `Lab` instance called, for example "Private Pei", and a new `Group` "Pei" to which "Private Pei" and those group members could belong.

### Masquerading as a User
As an admin you will see all Groups, all Labs, all Projects. To debug authentication, it may be helpful to assign yourself to certain groups using the Admin interface and "masquerade" as a common user. The "View as" toggle in the Admin menu that allows you to view myBiC as a user or admin. This setting persists as a session.

![](https://dl.dropboxusercontent.com/u/4055239/admindropdown.png)

## Creating a Group and Lab
Go to http://mybic.chop.edu/admin/auth/group/

Select "Add group". Fill in the Group name.

Add Labs - the `name` can be quite fancy but the `slug` should consist of solely of letters, numbers, underscores or hyphens.

## Creating Users
http://mybic.chop.edu/admin/auth/user

Select "Add user". Use the Active Directory username. The password field will not be used by myBiC.

## Starting a project
Go to http://mybic.chop.edu/admin/labs/project/

Select "Add project". Follow the instructions. The directories you specify must exist and should be as specific (as far down the directory tree) as possible.
On the myBiC server our Isilon mount is called `/mnt/variome`. On variome and raboso it is called `/nas/is1`. On respublica it is called `/mnt/isilon/cbmi/variome/`.

By default, if you leave out the leading slash MyBiC will assume you mean `/mnt/variome/`, so `leipzig/err-rna-seq/` will be understood to mean `/mnt/variome/leipzig/err-rna-seq/'.

![](https://dl.dropboxusercontent.com/u/4055239/project_admin.png)

### Friends of BiG
You should always use the full path for these mounts to BiG-affiliated labs.
* `/mnt/cbttc` - Resnick Lab
* `/mnt/NGS_data` - Spinner Lab

## Updating a project
![](https://dl.dropboxusercontent.com/u/4055239/admindropdown.png)

The admin menu provides a shortcut to the project admin page.

To reload index and child pages from with the project, use the "Refresh project" menu item

## Creating an index page
Index pages can be files on the Isilon or simply web pages served by Github, and they can be HTML or Markdown (recommended).

## Autoflank
`autoflank` is a project option that automatically adds the correct template tags to your markdown or HTML document to ensure it displays correct on myBiC.
![](https://dl.dropboxusercontent.com/u/4055239/autoflank.png)

## Django Template tags
If you are not using "autoflank". The index page you point to will need the following tags at the top for navigation:
```
{% extends "base.html" %}

{% block content %}
```
and this one at the bottom:
```
{% endblock %}
```
## Using Markdown
Some or all of the index page can be written in [Markdown](daringfireball.net/projects/markdown/).
If not using `autoflank`, you will need to load the Markdown library and template tag.

```
{% extends "base.html" %}
{% load markdown_tags %}
{% block content %}
{% markdown %}
```

```
{% endmarkdown %}
{% endblock %}
```

HTML is valid within Markdown.

## Static links
When you create a project you specify an absolute path on the Isilon to the static directory where all your deliverables should reside.

![](https://dl.dropboxusercontent.com/u/4055239/staticdir.png)

This is assigned to the `SLINK` Django template variable which you can use in your index page.

So to link to a static file `/mnt/variome/leipzig/liming_err_rnaseq/src/raw_counts.tab.txt` the static directory should be set to `/mnt/variome/leipzig/liming_err_rnaseq/src/` and the link will look like:

```
<p><a href="{{ SLINK }}/raw_counts.tab.txt">Raw HT-Seq Counts</a></p>
```

### Example 
A fully working example index.html is provided here:
[index.html](https://github.research.chop.edu/BiG/mybic/wiki/Example-index.html)

### Implementation

When a project is created, one symlink is placed at `mybic/mybic/labs/templates/your_lab/your_project` that points to your index page and one is placed in `mybic/_site/static/your_lab/your_project` that points to static path your specify on the read-only Isilon mount.

### Using Github for Serving Content
[github.com](http://github.com), or our internal [github.research.chop.edu](https://github.research.chop.edu), is a functional website and can be used as:
* The source from which index files are copied onto the myBiC site
* A place to put static files (under 50MB)

#### Using Github for the index page
Simply specify the "raw" Github content (as opposed to "blob") hyperlink:
`https://github.research.chop.edu/BiG/MD_vs_ATRT/raw/master/index.md`

in the "Index page" field:

![hyperlink](https://dl.dropboxusercontent.com/u/4055239/hyperlink.png)

The content can be Markdown or HTML, but template tags are still required.

When using a hyperlink as the source, myBiC copies the content over, so _you will need to re-save your project to update the index page in myBiC_

### Child index pages
Often you may want to provide users with additional project detail pages that share the same navigation header as the main project index. Multiple "child index pages" can be created for any given project from the admin page. These use the same template tags as parents, and are provided an additional navigation layer within myBiC. 

#### How to create child pages
From the "Child Indices" section at the bottom of the project admin panel (Django administration), provide a disk or http link as you would for the parent index. Hit save.

Within the parent index html or markdown, refer to these children using their basenames. For example, `https://github.research.chop.edu/zhangz/autism_microarrays/raw/master/Control_kid-vs-Patient_kid.md` is referred to `Control_kid-vs-Patient_kid.md` from the parent index. Do not use `index.html` or `index.md` as names.

For every link in the parent index html or markdown to be treated as a child page, you need to add an index as above.

![](https://dl.dropboxusercontent.com/u/4055239/childindex.png)
#### Using Github for the static content
You can link out to static content that is stored in Github. The easiest way is to right click on the Github site to access the link, then replace "blob" with "raw":
`https://github.research.chop.edu/sassona/Demicco_ImmGen_v_Parclip/blob/master/B_GC_Sp_w_HuR_targets_subset_data_comparison.xlsx`

becomes:

`https://github.research.chop.edu/sassona/Demicco_ImmGen_v_Parclip/raw/master/B_GC_Sp_w_HuR_targets_subset_data_comparison.xlsx`

## Integration with knitr
knitr with Rmarkdown syntax combined with the `DT` library is a preferable method of creating myBiC compatible output.

Specify the `output: html_document`
```
---
title: "My knitr report"
author: "Jeremy Leipzig"
date: "May 28, 2015"
output: html_document
---
```

You should now see the knit icon in RStudio:
![](https://dl.dropboxusercontent.com/u/4055239/knit.png)

knitr blocks should specify `fig.path='{{SLINK}}/'`. This will create a directory called (unfortunately) `{{SLINK}}` for static content, and this variable as it is embedded in the HTML output will be evaluated to the static directory specified in your myBiC project configuration.

Images produced by knitr are saved but also converted to an inline [data URI scheme](https://en.wikipedia.org/wiki/Data_URI_scheme), but you can still provide links to those images.

```
```{r setup, echo=TRUE, message=FALSE, cache=FALSE, fig.path='{{SLINK}}/'}
```

The datatables library will produce client-side sortable tables that can be embedded in your knitr document
```
library(DT)
datatable(mtcars)
```

Ideally you should push the `.Rmd` and `.html` files to Github, and use the raw link in myBiC. Point your static directory to the `{{SLINK}}` directory in your project on the Isilon

![](https://dl.dropboxusercontent.com/u/4055239/staticslink.png)


##News
News can be at the site, lab, or project level. Markdown is accepted within the body.

![](https://dl.dropboxusercontent.com/u/4055239/site_article.png)