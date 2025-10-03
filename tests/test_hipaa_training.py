"""
Comprehensive Test Suite for HIPAA Training System
Run with: python test_hipaa_training.py
"""

import unittest
import json
import os
from datetime import datetime
from typing import Dict

# Import functions from main module
# Note: In real deployment, save the main code as hipaa_ai_pharmacy_production.py
# Then uncomment this import:
# from hipaa_ai_pharmacy_production import (
#     calculate_score, calculate_quiz_score, get_performance_feedback,
#     PASS_THRESHOLD, GOOD_THRESHOLD, PROGRESS_FILE
# )

# For testing purposes, replicate the functions here:
PASS_THRESHOLD = 80
GOOD_THRESHOLD = 60
PROGRESS_FILE = "hipaa_progress.json"

def calculate_score(responses: Dict[str, bool]) -> float:
    """Calculate percentage score from checklist responses."""
    completed = sum(responses.values())
    total = len(responses)
    return (completed / total) * 100 if total > 0 else 0.0

def calculate_quiz_score(correct_answers: int, total_questions: int) -> float:
    """Calculate quiz score percentage."""
    return (correct_answers / total_questions) * 100 if total_questions > 0 else 0.0

def get_performance_feedback(percentage: float) -> str:
    """Generate performance feedback based on score thresholds."""
    if percentage >= PASS_THRESHOLD:
        return "🎉 Excellent! You're HIPAA ready!"
    elif percentage >= GOOD_THRESHOLD:
        return "📚 Good effort! Review the lessons and try again."
    else:
        return "📖 Keep studying! Focus on the key concepts."


class TestScoreCalculation(unittest.TestCase):
    """Test score calculation functions"""
    
    def test_calculate_score_all_true(self):
        """Test score calculation with all items completed"""
        responses = {"item1": True, "item2": True, "item3": True}
        self.assertEqual(calculate_score(responses), 100.0)
    
    def test_calculate_score_all_false(self):
        """Test score calculation with no items completed"""
        responses = {"item1": False, "item2": False, "item3": False}
        self.assertEqual(calculate_score(responses), 0.0)
    
    def test_calculate_score_mixed(self):
        """Test score calculation with mixed responses"""
        responses = {"item1": True, "item2": False, "item3": True}
        expected = (2/3) * 100
        self.assertAlmostEqual(calculate_score(responses), expected, places=2)
    
    def test_calculate_score_empty(self):
        """Test score calculation with empty responses"""
        responses = {}
        self.assertEqual(calculate_score(responses), 0.0)
    
    def test_calculate_score_single_item(self):
        """Test score calculation with single item"""
        responses = {"item1": True}
        self.assertEqual(calculate_score(responses), 100.0)


class TestQuizScoreCalculation(unittest.TestCase):
    """Test quiz score calculation"""
    
    def test_quiz_perfect_score(self):
        """Test perfect quiz score"""
        self.assertEqual(calculate_quiz_score(5, 5), 100.0)
    
    def test_quiz_zero_score(self):
        """Test zero quiz score"""
        self.assertEqual(calculate_quiz_score(0, 5), 0.0)
    
    def test_quiz_partial_score(self):
        """Test partial quiz score"""
        self.assertEqual(calculate_quiz_score(3, 5), 60.0)
    
    def test_quiz_division_by_zero(self):
        """Test quiz score with zero questions"""
        self.assertEqual(calculate_quiz_score(0, 0), 0.0)
    
    def test_quiz_float_precision(self):
        """Test quiz score with decimal results"""
        result = calculate_quiz_score(2, 3)
        self.assertAlmostEqual(result, 66.666, places=2)


class TestPerformanceFeedback(unittest.TestCase):
    """Test performance feedback generation"""
    
    def test_feedback_excellent(self):
        """Test feedback for excellent performance"""
        feedback = get_performance_feedback(90)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_pass_threshold(self):
        """Test feedback at exact pass threshold"""
        feedback = get_performance_feedback(PASS_THRESHOLD)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_good(self):
        """Test feedback for good performance"""
        feedback = get_performance_feedback(70)
        self.assertIn("Good effort", feedback)
    
    def test_feedback_good_threshold(self):
        """Test feedback at exact good threshold"""
        feedback = get_performance_feedback(GOOD_THRESHOLD)
        self.assertIn("Good effort", feedback)
    
    def test_feedback_needs_improvement(self):
        """Test feedback for low performance"""
        feedback = get_performance_feedback(40)
        self.assertIn("Keep studying", feedback)
    
    def test_feedback_zero(self):
        """Test feedback for zero score"""
        feedback = get_performance_feedback(0)
        self.assertIn("Keep studying", feedback)
    
    def test_feedback_perfect(self):
        """Test feedback for perfect score"""
        feedback = get_performance_feedback(100)
        self.assertIn("Excellent", feedback)


class TestFileOperations(unittest.TestCase):
    """Test file save/load operations"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_file = "test_progress.json"
        # Clean up any existing test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Cleanup test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_progress(self):
        """Test saving progress to file"""
        test_data = {
            "checklist": {"item1": True, "item2": False},
            "timestamp": datetime.now().isoformat(),
            "percentage": 50.0
        }
        
        with open(self.test_file, "w") as f:
            json.dump(test_data, f)
        
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_progress(self):
        """Test loading progress from file"""
        test_data = {
            "checklist": {"item1": True, "item2": False},
            "percentage": 50.0
        }
        
        with open(self.test_file, "w") as f:
            json.dump(test_data, f)
        
        with open(self.test_file, "r") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data["percentage"], 50.0)
        self.assertEqual(loaded_data["checklist"]["item1"], True)
    
    def test_load_missing_file(self):
        """Test loading non-existent file raises error"""
        with self.assertRaises(FileNotFoundError):
            with open("nonexistent.json", "r") as f:
                json.load(f)
    
    def test_load_corrupted_json(self):
        """Test loading corrupted JSON raises error"""
        with open(self.test_file, "w") as f:
            f.write("This is not valid JSON {{{")
        
        with self.assertRaises(json.JSONDecodeError):
            with open(self.test_file, "r") as f:
                json.load(f)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_score_boundary_values(self):
        """Test score calculation at boundaries"""
        # Test 0%
        self.assertEqual(calculate_score({"a": False}), 0.0)
        
        # Test 100%
        self.assertEqual(calculate_score({"a": True}), 100.0)
    
    def test_large_checklist(self):
        """Test with large number of checklist items"""
        large_checklist = {f"item_{i}": i % 2 == 0 for i in range(100)}
        score = calculate_score(large_checklist)
        self.assertEqual(score, 50.0)
    
    def test_threshold_boundaries(self):
        """Test feedback at exact threshold boundaries"""
        # Just below pass threshold
        feedback1 = get_performance_feedback(PASS_THRESHOLD - 0.1)
        self.assertNotIn("Excellent", feedback1)
        
        # At pass threshold
        feedback2 = get_performance_feedback(PASS_THRESHOLD)
        self.assertIn("Excellent", feedback2)
        
        # Just below good threshold
        feedback3 = get_performance_feedback(GOOD_THRESHOLD - 0.1)
        self.assertIn("Keep studying", feedback3)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_complete_workflow(self):
        """Test complete checklist -> score -> feedback workflow"""
        # Simulate user completing checklist
        checklist = {
            "item1": True,
            "item2": True,
            "item3": False,
            "item4": True,
            "item5": True
        }
        
        # Calculate score
        score = calculate_score(checklist)
        self.assertEqual(score, 80.0)
        
        # Get feedback
        feedback = get_performance_feedback(score)
        self.assertIn("Excellent", feedback)
    
    def test_failing_workflow(self):
        """Test workflow with failing score"""
        checklist = {
            "item1": False,
            "item2": False,
            "item3": True,
            "item4": False,
            "item5": False
        }
        
        score = calculate_score(checklist)
        self.assertEqual(score, 20.0)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Keep studying", feedback)


def run_all_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestScoreCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestQuizScoreCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceFeedback))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
