# Privex CDN Builder

**CDN Builder** is a Python tool designed to ease the process of building CSS/JS libraries into minified files
that can be served via a CDN.

It automatically downloads each configured library via the appropriate download method (generally Git), then
generates the minified CSS/JS files. Each "library helper" in `cdnbuilder/libs` detects the version of the library
and it's sub-components (if it has any), allowing the generated files to be neatly organised by component/version.

Furthermore, if the library helper has `link_root` enabled, then the files within the versioned sub-folder will
automatically be symlinked to the libraries root output folder.

Example directory structure:

```bash

# After EOSJS is built by CDN builder, the compiled files are copied into the versioned sub-directory eosjs/20.0.1

$ ls -l output/eosjs/20.0.1

-rw-r--r--  1 chris  staff   39718 17 Oct 10:28 eosjs-api.js
-rw-r--r--  1 chris  staff   19052 17 Oct 10:28 eosjs-jsonrpc.js
-rw-r--r--  1 chris  staff  231136 17 Oct 10:28 eosjs-jssig.js
-rw-r--r--  1 chris  staff    9607 17 Oct 10:28 eosjs-numeric.js

# As EOSJS has link_root enabled, the files for the latest version (20.0.1) are automatically symlinked into
# the base output folder of EOSJS 

$ ls -l output/eosjs 

drwxr-xr-x  6 chris  staff  192 17 Oct 10:28 20.0.1
lrwxr-xr-x  1 chris  staff   88 17 Oct 10:28 eosjs-api.js -> /opt/cdn-builder/output/eosjs/20.0.1/eosjs-api.js
lrwxr-xr-x  1 chris  staff   92 17 Oct 10:28 eosjs-jsonrpc.js -> /opt/cdn-builder/output/eosjs/20.0.1/eosjs-jsonrpc.js
lrwxr-xr-x  1 chris  staff   90 17 Oct 10:28 eosjs-jssig.js -> /opt/cdn-builder/output/eosjs/20.0.1/eosjs-jssig.js
lrwxr-xr-x  1 chris  staff   92 17 Oct 10:28 eosjs-numeric.js -> /opt/cdn-builder/output/eosjs/20.0.1/eosjs-numeric.js

```

# Installation

Quickstart (Tested on Ubuntu Bionic 18.04 - may work on other Debian-based distros):

```
# Install dependencies
sudo apt update -y
sudo apt install -y git python3.7 python3.7-venv python3.7-dev

# Install pipenv if you don't already have it
pip3 install pipenv

# Install Yarn for handling most JS/CSS projects
curl --compressed -o- -L https://yarnpkg.com/install.sh | bash

# Clone the repo
git clone https://github.com/Privex/cdn-builder.git
cd cdn-builder

# Create a virtualenv + install required Python packages
pipenv install

# Enter the virtualenv, then build the libraries
pipenv shell
./run.py build
```

# License

This project is licensed under the **GNU AGPL v3**

For full details, please see `LICENSE.txt` and `AGPL-3.0.txt`.

Here's the important parts:

 - If you use this software (or substantial parts of it) to run a public service (including any separate user interfaces 
   which use it's API), **you must display a link to this software's source code wherever it is used**.
   
   Example: **This website uses the open source [Privex CDN Builder](https://github.com/Privex/cdn-builder)
   created by [Privex Inc.](https://www.privex.io)**
   
 - If you modify this software (or substantial portions of it) and make it available to the public in some 
   form (whether it's just the source code, running it as a public service, or part of one) 
    - The modified software (or portion) must remain under the GNU AGPL v3, i.e. same rules apply, public services must
      display a link back to the modified source code.
    - You must attribute us as the original authors, with a link back to the original source code
    - You must keep our copyright notice intact in the LICENSE.txt file

 - Some people interpret the GNU AGPL v3 "linking" rules to mean that you must release any application that interacts
   with our project under the GNU AGPL v3.
   
   To clarify our stance on those rules: 
   
   - If you have a completely separate application which simply sends API requests to a copy of Privex CDN Builder
     that you run, you do not have to release your application under the GNU AGPL v3. 
   - However, you ARE required to place a notice on your application, informing your users that your application
     uses Privex CDN Builder, with a clear link to the source code (see our example at the top)
   - If your application's source code **is inside of Privex CDN Builder**, i.e. you've added your own Python
     views, templates etc. to a copy of this project, then your application is considered a modification of this
     software, and thus you DO have to release your source code under the GNU AGPL v3.

 - There is no warranty. We're not responsible if you, or others incur any damages from using this software.
 
 - If you can't / don't want to comply with these license requirements, or are unsure about how it may affect
   your particular usage of the software, please [contact us](https://www.privex.io/contact/). 
   We may offer alternative licensing for parts of, or all of this software at our discretion.



# Contributing

We're very happy to accept pull requests, and work on any issues reported to us. 

Here's some important information:

**Reporting Issues:**

 - For bug reports, you should include the following information:
     - Version of the project you're using - `git log -n1`
     - The Python package versions you have installed - `pip3 freeze`
     - Your python3 version - `python3 -V`
     - Your operating system and OS version (e.g. Ubuntu 18.04, Debian 7)
 - For feature requests / changes
     - Clearly explain the feature/change that you would like to be added
     - Explain why the feature/change would be useful to us, or other users of the tool
     - Be aware that features/changes that are complicated to add, or we simply find un-necessary for our use of the tool 
       may not be added (but we may accept PRs)
    
**Pull Requests:**

 - We'll happily accept PRs that only add code comments or README changes
 - Use 4 spaces, not tabs when contributing to the code
 - You can use features from Python 3.4+ (we run Python 3.7+ for our projects)
    - Features that require a Python version that has not yet been released for the latest stable release
      of Ubuntu Server LTS (at this time, Ubuntu 18.04 Bionic) will not be accepted. 
 - Clearly explain the purpose of your pull request in the title and description
     - What changes have you made?
     - Why have you made these changes?
 - Please make sure that code contributions are appropriately commented - we won't accept changes that involve 
   uncommented, highly terse one-liners.

**Legal Disclaimer for Contributions**

Nobody wants to read a long document filled with legal text, so we've summed up the important parts here.

If you contribute content that you've created/own to projects that are created/owned by Privex, such as code or 
documentation, then you might automatically grant us unrestricted usage of your content, regardless of the open source 
license that applies to our project.

If you don't want to grant us unlimited usage of your content, you should make sure to place your content
in a separate file, making sure that the license of your content is clearly displayed at the start of the file 
(e.g. code comments), or inside of it's containing folder (e.g. a file named LICENSE). 

You should let us know in your pull request or issue that you've included files which are licensed
separately, so that we can make sure there's no license conflicts that might stop us being able
to accept your contribution.

If you'd rather read the whole legal text, it should be included as `privex_contribution_agreement.txt`.

# Thanks for reading!

**If this project has helped you, consider [grabbing a VPS or Dedicated Server from Privex](https://www.privex.io) -**
**prices start at as little as US$8/mo (we take cryptocurrency!)**
