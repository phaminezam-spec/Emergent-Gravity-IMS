import numpy as np


def run_structural_audit(expansion_factor=3.0):
    """
    Structural audit comparing two connectivity scaling regimes
    under accelerated expansion.

    Purpose
    -------
    Evaluates relative connectivity stability between:
    1. A continuum-style decay relationship
    2. A logarithmic reinforcement relationship

    Parameters
    ----------
    expansion_factor : float, optional
        Dimensionless expansion parameter used to evaluate scaling behavior.

    Returns
    -------
    dict
        Computed integrity metrics for both regimes.

    Notes
    -----
    This function is intended as a comparative diagnostic tool for
    evaluating alternative connectivity scaling assumptions.
    """

    # Reference scaling constants
    continuum_scale = 1.22
    lattice_scale = 1.52

    # Continuum-style decay relationship
    continuum_integrity = continuum_scale / np.sqrt(expansion_factor)

    # Logarithmic reinforcement relationship
    lattice_integrity = lattice_scale * (1.0 + np.log(expansion_factor))

    results = {
        "expansion_factor": expansion_factor,
        "continuum_integrity": continuum_integrity,
        "lattice_integrity": lattice_integrity
    }

    return results


if __name__ == "__main__":

    audit = run_structural_audit()

    print(f"--- STRUCTURAL AUDIT @ expansion={audit['expansion_factor']} ---")
    print(f"Continuum scaling metric: {audit['continuum_integrity']:.3f}")
    print(f"Lattice scaling metric: {audit['lattice_integrity']:.3f}")

    if audit["lattice_integrity"] > audit["continuum_integrity"]:
        print("\nObservation: logarithmic scaling produces higher connectivity metric under these conditions.")
