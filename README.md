# zk-ssg

This is a static site generator (SSG) for [zettelkastens](https://blog.viktomas.com/posts/slip-box/), which means it converts markdown-based zettelkastens into fully functional HTML and CSS files that can be immediately published as a website. This program **_never_** makes any changes to the files in the zettelkasten; it only copies the relevant files to the site folder and works with those copies.

[Here's a site that was built with this program.](https://wheelercj.github.io/notes/)

[Comparisons to other methods for publishing a zettelkasten.](https://wheelercj.github.io/notes/pages/20210510123255.html)

Feature requests, contributions, etc. are welcome!

## Features
* After setup (instructions below), you can add more pages to your site by simply adding the `#published` tag to your markdown files and running this program again.
* All internal links are converted to HTML, regardless of whether they are markdown-style links or zettelkasten-style links.
* A settings menu makes the site's title, colors, and other important options easy to customize. Also, the CSS and the HTML that wraps each page's content can optionally be customized directly. When you generate the site the first time, `style.css`, `header.html`, and `footer.html` will be created and then reused in the future.
* Three index pages listing all the other pages are automatically populated: categorical, alphabetical, and chronological indexes.
* Any broken internal links and internal links with outdated titles will be detected.
* Any file attachments in the #published pages will be automatically copied to the site folder.
* This program is 100% compatible with [Zettlr](https://www.zettlr.com/)'s default settings for internal links and file names, and may be compatible with other markdown editors as well.

## Current limitations
* The only markdown files you can publish that have alphabetic characters in their file names are `index.md` and `about.md`. The names of all the other markdown files you want to publish must be 14-digit numbers followed by `.md`, e.g. `20201221140928.md`. The number represents the time of the file's creation in the YYYYMMDDhhmmss format.
* Internal links are double square brackets surrounding a 14-digit number, followed by the file's title (its first header), e.g. `[[20201221140928]] this is the title`. The link's 14-digit number is the same as the linked file's name.

## Setup
1. Create a new folder that will hold your website's files (the "site folder").
2. In your zettelkasten folder, create `index.md` and `about.md`. `index.md` will later become your site's homepage, and has special options explained in the next steps. You can write whatever you would like in `about.md`.
3. In your zettelkasten folder, add the `#published` tag to each markdown file that you want to publish, including `index.md` and `about.md`. Only files with this tag will be copied to the site folder.
4. In `index.md`, add other tags for the categories of zettels you want links to be listed for. When zk-ssg makes a copy of `index.md`, in that copy, it will automatically replace each of the tags (except `#published`) with links to zettels that also have that same tag. Any headers, empty lines, etc. you added to the file around the tags will be kept, so you will probably want to spread the tags out. [Here's](https://gist.github.com/wheelercj/f5a974277f2d6096471a88a2c27562f0) an example of how you can write `index.md`.
5. Run this program. Now you're ready to send your new HTML files to your site's host! If you don't have one yet, [GitHub Pages](https://pages.github.com/) is worth considering.

## What gets overwritten or deleted?
### Short answer
* **_Nothing_** in the zettelkasten folder is changed in any way.
* Site files with the same name as zettelkasten files get overwritten.
* All markdown files in the site folder's pages folder that do not get overwritten get deleted.
* The program will ask to delete HTML files that were not overwritten.
* Some markdown files in the site folder (outside the pages folder) may be overwritten, depending on their names.

### Detailed answer
When the site files are being generated, all currently existing markdown and HTML files in the site folder that happen to have the same name as any markdown files in the zettelkasten folder that contain the `#published` tag will be overwritten. The program will not overwrite `style.css` (except for user settings changes), `header.html`, and `footer.html`, and will create them only if they do not already exist. Any markdown files in the site folder's pages folder that do not get overwritten will be deleted. Specific markdown files in the site folder (outside the pages folder) will get overwritten: `index.md`, `about.md`, `alphabetical-index.md`, and `chronological-index.md`. If there are HTML files in the site folder that do not get overwritten, the program will ask to delete them unless their absolute paths are listed in a file in the site folder named `ssg-ignore.txt`, each file path on its own line.
