"""Smoke tests for the Terraform module Copier template."""

import subprocess
from pathlib import Path

import pytest


def test_generate_with_defaults(copie):
    """Test basic template generation with minimal answers."""

    result = copie.copy(
        extra_answers={
            "module_name": "test_module",
            "description": "Test module",
            "author_full_name": "John Doe",
            "github_user_name": "jdoe",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    module_dir = result.project_dir
    assert (module_dir / "main.tf").exists()
    assert (module_dir / "outputs.tf").exists()
    assert (module_dir / "variables.tf").exists()
    assert (module_dir / "versions.tf").exists()
    assert (module_dir / "README.md").exists()
    assert (module_dir / "LICENSE").exists()


@pytest.mark.parametrize(
    "include_examples,include_terratest",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_conditional_directories(copie, include_examples, include_terratest):
    """Test that conditional directories are generated correctly."""
    result = copie.copy(
        extra_answers={
            "module_name": "test_module",
            "description": "Test module",
            "author_full_name": "John Doe",
            "github_user_name": "jdoe",
            "include_examples": include_examples,
            "include_terratest": include_terratest,
        }
    )
    assert result.exit_code == 0

    module_dir = result.project_dir
    examples_dir = module_dir / "examples"
    test_dir = module_dir / "test"

    # Check examples
    if include_examples:
        assert examples_dir.exists()
        assert (examples_dir / "complete" / "main.tf").exists()
    else:
        assert not examples_dir.exists()

    # Check terratest
    if include_terratest:
        assert test_dir.exists()
        assert (test_dir / "Makefile").exists()
        assert (test_dir / "test_module_test.go").exists()
    else:
        assert not test_dir.exists()


def test_terraform_validate(copie):
    """Test that generated Terraform is syntactically valid."""
    result = copie.copy(
        extra_answers={
            "module_name": "test_module",
            "description": "Test module",
            "author_full_name": "John Doe",
            "github_user_name": "jdoe",
        }
    )
    assert result.exit_code == 0

    module_dir = result.project_dir

    # Run terraform validate (requires terraform CLI)
    try:
        output = subprocess.run(
            "terraform init; terraform validate",
            cwd=module_dir,
            capture_output=True,
            text=True,
            timeout=20,
            shell=True,
        )
        assert output.returncode == 0, f"terraform validate failed: {output.stderr}"
    except FileNotFoundError:
        pytest.skip("terraform CLI not available")
