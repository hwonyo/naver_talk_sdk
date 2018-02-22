## How to contribute to NaverTalk SDK for Python project

Thank you so much for taking your time to contribute. Let's make a stress-less world together! 
NaverTalk SDK for Python is not very different from any other opensource projects. 
It will be amazing if you could help us by doing any of the following:

- File an issue in [the issue tracker](https://github.com/HwangWonYo/naver_talk_sdk/issues) to report bugs and propose new features and
  improvements.
- Ask a question using [the issue tracker](https://github.com/HwangWonYo/naver_talk_sdk/issues).
- Contribute your work by sending [a pull request](https://github.com/HwangWonYo/naver_talk_sdk/pulls).

## Development Guide

1. register an **issue**

2. **synchronize master branch and create issue-branch**

   ```
   git fetch
   git checkout -b <issue-branch> origin/master
   ```

   - prefix of branch name: **issue**
     - ex) issue_modify_button_template

3. **develop code**

4. **rebase**

   ```
   git rebase origin/develop
   git push origin <branch>
   ```

5. **pull-request**

   - base: **master** <= compare: < issue-branch >
