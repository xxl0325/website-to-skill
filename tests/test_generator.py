"""Tests for skill generator."""

import tempfile
from pathlib import Path
from generator.skill_md import generate_skill
from generator.design_ref import generate_design_ref
from scraper.analyzer import DesignData


def test_generate_skill():
    """Test SKILL.md generation."""
    design = DesignData(
        colors={"primary": "#3E6AE1"},
        fonts={"family": "Inter"},
        buttons={"background": "#3E6AE1"},
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        path = generate_skill("test", design, tmpdir)
        assert Path(path).exists()


def test_generate_design_ref():
    """Test design.md generation."""
    design = DesignData(
        colors={"primary": "#3E6AE1"},
        fonts={"family": "Inter"},
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        path = generate_design_ref("test", design, tmpdir)
        assert Path(path).exists()
