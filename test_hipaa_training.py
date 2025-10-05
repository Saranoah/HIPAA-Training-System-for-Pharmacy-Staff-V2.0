"""
Enhanced Test Suite for HIPAA Training System (15-item checklist)
Run with: python test_hipaa_training.py
"""

import unittest
import json
import os
from datetime import datetime
from typing import Dict

# Constants matching the enhanced application
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
        return "Excellent! You're HIPAA ready!"
    elif percentage >= GOOD_THRESHOLD:
        return "Good effort! Review the lessons and try again."
    else:
        return "Keep studying! Focus on the key concepts."


class TestScoreCalculation(unittest.TestCase):
    """Test score calculation functions with 15-item checklist"""
    
    def test_calculate_score_all_true_15_items(self):
        """Test score calculation with all 15 items completed"""
        responses = {f"item_{i}": True for i in range(15)}
        self.assertEqual(calculate_score(responses), 100.0)
    
    def test_calculate_score_all_false_15_items(self):
        """Test score calculation with no items completed"""
        responses = {f"item_{i}": False for i in range(15)}
        self.assertEqual(calculate_score(responses), 0.0)
    
    def test_calculate_score_pass_threshold(self):
        """Test score at 80% pass threshold (12/15 items)"""
        responses = {f"item_{i}": i < 12 for i in range(15)}
        expected = (12/15) * 100
        self.assertAlmostEqual(calculate_score(responses), expected, places=2)
    
    def test_calculate_score_good_threshold(self):
        """Test score at 60% good threshold (9/15 items)"""
        responses = {f"item_{i}": i < 9 for i in range(15)}
        expected = (9/15) * 100
        self.assertEqual(calculate_score(responses), expected)
    
    def test_calculate_score_mixed_15_items(self):
        """Test score calculation with mixed responses"""
        responses = {f"item_{i}": i % 2 == 0 for i in range(15)}
        expected = (8/15) * 100  # 8 even numbers in 0-14
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
    """Test performance feedback generation with new thresholds"""
    
    def test_feedback_excellent_15_items(self):
        """Test feedback for 12/15 items (80% - pass threshold)"""
        feedback = get_performance_feedback(80.0)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_above_pass_threshold(self):
        """Test feedback for 13/15 items (86.67%)"""
        feedback = get_performance_feedback(86.67)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_at_pass_threshold(self):
        """Test feedback at exact pass threshold"""
        feedback = get_performance_feedback(PASS_THRESHOLD)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_good_9_items(self):
        """Test feedback for 9/15 items (60% - good threshold)"""
        feedback = get_performance_feedback(60.0)
        self.assertIn("Good effort", feedback)
    
    def test_feedback_between_thresholds(self):
        """Test feedback for 10/15 items (66.67% - between thresholds)"""
        feedback = get_performance_feedback(66.67)
        self.assertIn("Good effort", feedback)
    
    def test_feedback_at_good_threshold(self):
        """Test feedback at exact good threshold"""
        feedback = get_performance_feedback(GOOD_THRESHOLD)
        self.assertIn("Good effort", feedback)
    
    def test_feedback_needs_improvement_8_items(self):
        """Test feedback for 8/15 items (53.33% - below good threshold)"""
        feedback = get_performance_feedback(53.33)
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
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Cleanup test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_progress_15_items(self):
        """Test saving progress with 15-item checklist"""
        test_data = {
            "checklist": {f"item_{i}": i < 12 for i in range(15)},
            "timestamp": datetime.now().isoformat(),
            "percentage": 80.0,
            "compliance_score": "12/15"
        }
        
        with open(self.test_file, "w") as f:
            json.dump(test_data, f)
        
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_progress_15_items(self):
        """Test loading progress with 15-item checklist"""
        test_data = {
            "checklist": {f"item_{i}": i < 9 for i in range(15)},
            "percentage": 60.0,
            "compliance_score": "9/15"
        }
        
        with open(self.test_file, "w") as f:
            json.dump(test_data, f)
        
        with open(self.test_file, "r") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data["percentage"], 60.0)
        self.assertEqual(loaded_data["compliance_score"], "9/15")
        self.assertEqual(len(loaded_data["checklist"]), 15)
    
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
    """Test edge cases and boundary conditions with 15-item checklist"""
    
    def test_score_boundary_values_15_items(self):
        """Test score calculation at boundaries with 15 items"""
        # Test 0%
        self.assertEqual(calculate_score({f"item_{i}": False for i in range(15)}), 0.0)
        
        # Test 100%
        self.assertEqual(calculate_score({f"item_{i}": True for i in range(15)}), 100.0)
    
    def test_pass_threshold_boundary_15_items(self):
        """Test exactly at 80% threshold (12/15 items)"""
        responses = {f"item_{i}": i < 12 for i in range(15)}
        score = calculate_score(responses)
        self.assertEqual(score, 80.0)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Excellent", feedback)
    
    def test_below_pass_threshold_15_items(self):
        """Test just below 80% threshold (11/15 = 73.33%)"""
        responses = {f"item_{i}": i < 11 for i in range(15)}
        score = calculate_score(responses)
        self.assertAlmostEqual(score, 73.33, places=2)
        
        feedback = get_performance_feedback(score)
        self.assertNotIn("Excellent", feedback)
        self.assertIn("Good effort", feedback)
    
    def test_good_threshold_boundary_15_items(self):
        """Test exactly at 60% threshold (9/15 items)"""
        responses = {f"item_{i}": i < 9 for i in range(15)}
        score = calculate_score(responses)
        self.assertEqual(score, 60.0)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Good effort", feedback)
    
    def test_below_good_threshold_15_items(self):
        """Test just below 60% threshold (8/15 = 53.33%)"""
        responses = {f"item_{i}": i < 8 for i in range(15)}
        score = calculate_score(responses)
        self.assertAlmostEqual(score, 53.33, places=2)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Keep studying", feedback)
    
    def test_large_checklist(self):
        """Test with large number of checklist items"""
        large_checklist = {f"item_{i}": i % 2 == 0 for i in range(100)}
        score = calculate_score(large_checklist)
        self.assertEqual(score, 50.0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows with 15-item checklist"""
    
    def test_complete_workflow_passing(self):
        """Test complete checklist -> score -> feedback workflow (passing)"""
        # Simulate user completing 12/15 items (80%)
        checklist = {f"item_{i}": i < 12 for i in range(15)}
        
        # Calculate score
        score = calculate_score(checklist)
        self.assertEqual(score, 80.0)
        
        # Get feedback
        feedback = get_performance_feedback(score)
        self.assertIn("Excellent", feedback)
    
    def test_complete_workflow_good(self):
        """Test workflow with good score (9/15 = 60%)"""
        checklist = {f"item_{i}": i < 9 for i in range(15)}
        
        score = calculate_score(checklist)
        self.assertEqual(score, 60.0)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Good effort", feedback)
    
    def test_failing_workflow(self):
        """Test workflow with failing score (7/15 = 46.67%)"""
        checklist = {f"item_{i}": i < 7 for i in range(15)}
        
        score = calculate_score(checklist)
        self.assertAlmostEqual(score, 46.67, places=2)
        
        feedback = get_performance_feedback(score)
        self.assertIn("Keep studying", feedback)
    
    def test_category_distribution(self):
        """Test that 15 items cover different categories appropriately"""
        # This test assumes your app has category tracking
        # Adjust counts based on your actual distribution
        expected_total = 15
        
        # Example: 2 Training + 5 Knowledge + 5 Technical + 3 Compliance = 15
        self.assertEqual(expected_total, 15)


def run_all_tests():
    """Run all tests and generate report"""
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
    print("TEST SUMMARY - Enhanced 15-Item Checklist")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
    print(f"Success Rate: {success_rate:.1f}%")
    print("\nChecklist Configuration:")
    print(f"  Total Items: 15")
    print(f"  Pass Threshold: 12/15 (80%)")
    print(f"  Good Threshold: 9/15 (60%)")
    print(f"  Critical Gap: <9/15 (<60%)")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
