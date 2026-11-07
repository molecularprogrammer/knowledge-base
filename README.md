# Molecular Programmer Knowledge Base

An overview of the project can be found [here](/docs/index.md).

Developer information can be found [here](/docs/contribute.md).

---

## Dependencies

The development environment is containerized, and requires Docker Compose to use.

Refer to [the official documentation](https://docs.docker.com/get-started/) for installation
instructions.

The official installation and setup documentation is rather fragmented, so you can optionally use
the following convenience scripts:

- On Ubuntu-based Linux distros, run `sudo ./install_docker.sh`

---

## Run Tasks

Run `./task.sh` to see the available project tasks. Tasks run in the base development container.

---

## Language Model Assistance

See [the Cline architecture and usage guide](.cline/.arch.md) for why this template uses Cline,
how to use it, and how to configure its optional local proxy.

---

## Documentation

Documentation is intended to enable self-onboarding. Tribal knowledge should not be required.

### Developer-Only Documentation

The contents of this repo are documented in a heirarchy of repository architecture files
(*.arch.md) that live alongside the files they are most closely related to. This meta data can help
other developers (as well as language models) quickly understand the high-level intent and usage of
all folders and files.

The project architecture documentation in the [documentation folder](documentation) describes the
system from a requirements and externally observable perspective. This documentation describes how
those requirements are realized by the implementation in this repository. The two therefore
complement rather than duplicate one another.

Since IDEs like VSCode allow previewing rendered markdown, there is no need to "build"
this developer-only code architecture documentation, but it can optionally link back to the project
documentation for traceability, similar to code.

Start with the [root repo architecture document](.arch.md).

---

## Git Workflows

### Branches

Typically use one branch per work item.

### Merges

Changes get merged directly to the ‘main’ branch, which is used for production deployment.

Merges to ‘main’ are only possible through Pull Requests, which enforces reviews/approvals, and
shows pull request branch pipeline success status that encapsulates all automated checks. (A more
complex branching strategy can be introduced at any time, as the need arises.)

Prefer semi-linear merge to keep a clean Git history, while ensuring file change history is not
obfuscated by a move and squash.

### Pull Requests

Code reviews should generally be self-explanatory, with only a link to the issue tracker, and
whatever information is in the PR branch. If they are not self-explanatory, consider
updating the project documentation.
