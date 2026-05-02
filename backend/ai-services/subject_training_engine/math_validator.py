# ai-services/subject_training_engine/math_validator.py
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import mpmath
from mpmath import mp, iv, mpf
import logging

# Configure mpmath for high precision (e.g., 50 decimal places)
mp.dps = 50

def validate_math(expression: str, steps: list) -> dict:
    """
    Original symbolic validation using SymPy.
    Validates that each step follows logically from the previous.
    """
    transformations = (standard_transformations + (implicit_multiplication_application,))
    try:
        final_expr = parse_expr(expression, transformations=transformations)
        simplified_final = sympy.simplify(final_expr)

        previous = None
        for i, step in enumerate(steps):
            try:
                current = parse_expr(step, transformations=transformations)
                if previous is not None:
                    if not sympy.simplify(current - previous) == 0:
                        return {
                            "is_correct": False,
                            "simplified_expression": str(simplified_final),
                            "error_step": i,
                            "feedback": f"Step {i+1} does not follow from previous step."
                        }
                previous = current
            except Exception as e:
                return {
                    "is_correct": False,
                    "simplified_expression": str(simplified_final),
                    "error_step": i,
                    "feedback": f"Step {i+1} is not a valid expression: {str(e)}"
                }

        return {
            "is_correct": True,
            "simplified_expression": str(simplified_final),
            "error_step": None,
            "feedback": "All steps are mathematically consistent."
        }
    except Exception as e:
        return {
            "is_correct": False,
            "simplified_expression": None,
            "error_step": 0,
            "feedback": f"Could not parse expression: {str(e)}"
        }

def validate_numerical(expression: str, expected_range: tuple = None, tolerance: str = "1e-15"):
    """
    Validate a numerical expression using arbitrary‑precision arithmetic.
    
    Args:
        expression: string like "sin(pi/4) + 2**0.5"
        expected_range: optional (low, high) tuple for interval validation
        tolerance: string representation of acceptable error (e.g., "1e-15")
    
    Returns:
        dict with evaluation result and validation info.
    """
    try:
        # Evaluate with mpmath
        result = mpmathify(expression)
        
        # Convert tolerance to mpf
        tol = mpf(tolerance)
        
        # If expected range provided, check if result lies within it
        if expected_range:
            low, high = mpf(expected_range[0]), mpf(expected_range[1])
            in_range = (low <= result <= high)
            interval_result = iv.mpf([low, high])
            within = result in interval_result
            return {
                "value": str(result),
                "high_precision_value": str(result),
                "interval_check": {
                    "expected_range": f"[{low}, {high}]",
                    "result_in_range": bool(within)
                },
                "is_valid": bool(within)
            }
        else:
            return {
                "value": str(result),
                "high_precision_value": str(result),
                "is_valid": True
            }
    except Exception as e:
        logging.error(f"Numerical validation error: {e}")
        return {
            "is_valid": False,
            "error": str(e)
        }

def compare_algorithms_output(algorithm1_expr: str, algorithm2_expr: str, precision: int = 100):
    """
    Compare the numerical output of two algorithms (expressions).
    Useful for analyzing different solution approaches.
    """
    mp.dps = precision
    try:
        res1 = mpmathify(algorithm1_expr)
        res2 = mpmathify(algorithm2_expr)
        diff = abs(res1 - res2)
        return {
            "algorithm1_result": str(res1),
            "algorithm2_result": str(res2),
            "difference": str(diff),
            "are_equivalent": diff < mpf("1e-50")  # extremely strict
        }
    except Exception as e:
        return {"error": str(e)}

# Helper to safely convert string to mpmath expression
def mpmathify(expr: str):
    """Convert a string to an mpmath expression (supports functions like sin, pi)."""
    # mpmath's own parser can be used, but for simplicity we use sympy then convert.
    # However, sympy may not support all mpmath special functions. 
    # We'll use mpmath's own parser if possible.
    # mpmath has a 'sympify' like function? Actually mpmath works with strings directly in many cases.
    # Safer: use sympy to parse and then convert to mpmath via evalf.
    # But that may lose mpmath-specific functions. We'll keep it simple and use mpmath's conversion.
    # mpmath's mpf and functions are callable; we can eval with a safe namespace.
    # For security, we should restrict the namespace.
    safe_dict = {
        'sin': mpmath.sin, 'cos': mpmath.cos, 'tan': mpmath.tan,
        'asin': mpmath.asin, 'acos': mpmath.acos, 'atan': mpmath.atan,
        'sinh': mpmath.sinh, 'cosh': mpmath.cosh, 'tanh': mpmath.tanh,
        'exp': mpmath.exp, 'log': mpmath.log, 'log10': mpmath.log10,
        'sqrt': mpmath.sqrt, 'pi': mpmath.pi, 'e': mpmath.e,
        'gamma': mpmath.gamma, 'zeta': mpmath.zeta, 'erf': mpmath.erf,
        'factorial': mpmath.factorial, 'binomial': mpmath.binomial,
        'mpf': mpmath.mpf, 'mpc': mpmath.mpc,
        'iv': mpmath.iv  # interval arithmetic
    }
    # Evaluate the expression with these functions
    return eval(expr, {"__builtins__": {}}, safe_dict)