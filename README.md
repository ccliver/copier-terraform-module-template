# Copier Template for AWS Terraform Modules

A [Copier](https://copier.readthedocs.io/en/stable/) template that scaffolds opinionated boilerplate for AWS Terraform modules, including CI, linting, security scanning, and optional Terratest integration.

[![CI](https://github.com/ccliver/copier-terraform-module-template/actions/workflows/ci.yml/badge.svg)](https://github.com/ccliver/copier-terraform-module-template/actions/workflows/ci.yml)

## Prerequisites

- [Copier](https://copier.readthedocs.io/en/stable/) >= 9
- [Git](https://git-scm.com/)

## Usage

```bash
copier copy https://github.com/ccliver/copier-terraform-module-template ./terraform-aws-<module-name>
```

Copier will prompt for the following inputs:

| Variable | Description | Default |
|---|---|---|
| `aws_provider_version` | AWS provider version constraint | `~> 6` |
| `module_name` | Short module name (e.g. `vpc`, `eks-cluster`) | — |
| `description` | A short description of the module | — |
| `author_full_name` | Your full name | — |
| `github_user_name` | Your GitHub username | — |
| `copyright_holder` | Name or organization for the MIT license | `author_full_name` |
| `copyright_year` | Year for the copyright notice | `2026` |
| `include_terratest` | Scaffold a Terratest test file | `true` |
| `include_examples` | Scaffold an `examples/` directory | `true` |

## What Gets Generated

```
terraform-aws-<module-name>/
├── .github/
│   └── workflows/
│       ├── ci.yml           # PR workflow: runs pre-commit on changed files
│       └── release.yml      # Release workflow: semantic-release on push to main
├── .gitignore
├── .pre-commit-config.yaml  # terraform_fmt, validate, docs, tflint, trivy
├── .tflint.hcl              # TFLint with the AWS ruleset
├── LICENSE                  # MIT license
├── main.tf
├── outputs.tf
├── variables.tf
├── examples/                # (optional) complete usage example
│   └── complete/
└── test/                    # (optional) Terratest skeleton
    └── <module_name>_test.go
```

## What's Included

### CI (`ci.yml`)

A GitHub Actions workflow triggers on every pull request and runs `pre-commit` against changed files using the [`pre-commit-terraform`](https://github.com/antonbabenko/pre-commit-terraform) Docker image.

### Pre-commit hooks (`.pre-commit-config.yaml`)

| Hook | Purpose |
|---|---|
| `terraform_fmt` | Enforce consistent formatting |
| `terraform_validate` | Validate configuration syntax |
| `terraform_docs` | Auto-generate and update module documentation |
| `terraform_tflint` | Lint against AWS best-practice rules |
| `terraform_trivy` | Scan for MEDIUM/HIGH/CRITICAL security misconfigurations |
| `check-merge-conflict` | Catch unresolved merge conflict markers |
| `end-of-file-fixer` | Ensure files end with a newline |

### TFLint (`.tflint.hcl`)

Configured with the [tflint-ruleset-aws](https://github.com/terraform-linters/tflint-ruleset-aws) plugin.

### Terratest (`test/<module_name>_test.go`)

An optional Go test skeleton using [Terratest](https://terratest.gruntwork.io/) that runs `terraform init && apply` against the `examples/complete` directory and defers a `destroy`.

## Updating a Generated Module

To pull in upstream template changes after the initial generation:

```bash
cd terraform-aws-<module-name>
copier update
```

## License

MIT
