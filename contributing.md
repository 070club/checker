# Contributing

Thank you for your interest in contributing to the 070club Checkers (endorsements, scorers, etc).
<strong>We love pull requests from everyone. Here's how you can help!</strong>

## GitHub Issue Tracker

* 070club uses the [Github issue tracker](https://github.com/070club/checker/issues) as the main venue for
bug reports, feature requests, enhancement requests, and pull requests.

## Bug Reports

We love good bug reports!  A good bug report is:
* Specific: Ideally somebody can fix the bug without needing to figure our where to look.  
* Actionable: Knowing what was expected vs. what actually happened is critical.
* Not a duplicate: Please search the existing issues to see if this has already been reported
* Environmental: Please indicate the OS and version you are using.  If you have multiple OSes avaialble knowing if this is specific to one operating system or version of operating system is helpful.

Yes, this is a lot to ask for, but the more specific bug reports are, the more quickly someone can grab it and fix it.  As much (or as little) information you have helps, but the more the merrier and the more likely it'll get quicky fixed.

## Pull Requests

We love Pull Requests! Good pull requests for features, enhancements and bug reports are the key to any open source project. Ideally they will also solve or implement one feature, enhancement request or bug report so it is easy to merge, and in the case of problems, revert. 

<strong>Please talk to us first</strong> before you spend a nontrivial amount of time on a new coding project.  We're happy to help offer suggestions, help vet design ideas, and also warn about gotchas in the code before you wander down a path that can cause problems that can keep a PR from being merged.  

Here's the best way to work with the 070club git repository:

1. [Fork](https://help.github.com/articles/fork-a-repo/), then clone your fork, and configure the remotes:
    
    ```bash
    # Create a directory for your fork's clone.
    mkdir git
    chdir git
    # Clone your fork into the current directory (git).
    # Use your GitHub username instead of <em>YOUR-USERNAME</em>
    git clone https://github.com/<em>YOUR-USERNAME</em>/checker.git
    # Change directory into the wwiv directory of your clone/
    chdir checker
    # Add the remotes for the upstream repository (070club/checker)
    git remote add upstream https://github.com/070club/checker.git
    ```
    
2. If you have done step 1 a while ago, pull from the upstream repository to update your clone with the latest from 070club/checker.
    ```bash
    # make sure your branch is back onto the "master" branch
    git checkout master
    # pull (this is a fetch + merge) in the changes from the 070club/checker respository.
    git pull upstream master
    # push the changes from 070club/checker to your fork on github.
    git push
    ```
    
3. Create a new branch off of master for your feature, enhancement, or bug fix and let GitHub know about your branch.

    ```bash
    git checkout -b <MY-BRANCH-NAME>
    git push origin <MY-BRANCH-NAME>
    ```    

4. Make your changes by editing the files and committing changes to your local repository.  Please use good commit messages that explain the changes and also reference github issues as necessary.

5. Merge any new changes from the 070club/checker respository into your development branch

    ```bash
    git pull upstream master
    ```    
    
6. Push your changes from your local machine to your fork on github.

    ```bash
    git push origin <MY-BRANCH-NAME>
    ```
    
7. Open a [Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear and concise
   title and description of the changes.  Please reference any issues on GitHub as needed. 
   [pr]: https://github.com/070club/checker/compare

8. At this point you're waiting on us. We will endeavour to approve requests or comment within a week.
Please remember this is a just hobby. :-) We may suggest
some changes or improvements or alternatives to your suggestions or approve them outright.

9. Some things that will increase the chance that your pull request is accepted:

* Fix an open issue.
* Write a [good commit message][commit].
* Explain how you tested the changes, any known limitations, etc.

[commit]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
