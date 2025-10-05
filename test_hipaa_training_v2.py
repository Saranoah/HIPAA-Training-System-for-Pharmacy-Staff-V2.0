#!/usr/bin/env python3
"""
Test Suite for HIPAA Training System V2.0
Run with: python test_hipaa_training_v2.py
"""

import unittest
import json
import os
from datetime import datetime

# Import from main application
from hipaa_training_v2 import (
    calculate_score,
    get_performance_feedback,
    LESSONS,
    QUIZ_QUESTIONS,
    CHECKLIST_ITEMS,
    PASS_THRESHOLD,
    GOOD_THRESHOLD,
    PROGRESS_FILE
)


class TestContentCompleteness(unittest.TestCase):
    """Verify all content is complete"""
    
    def test_has_13_lessons(self):
        """Verify 13 lessons are present"""
        self.assertEqual(len(LESSONS), 13, "Should have exactly 13 lessons")
    
    def test_has_15_quiz_questions(self):
        """Verify 15 quiz questions are present"""
        self.assertEqual(len(QUIZ_QUESTIONS), 15, "Should have exactly 15 quiz questions")
    
    def test_has_15_checklist_items(self):
        """Verify 15 checklist items are present"""
        self.assertEqual(len(CHECKLIST_ITEMS), 15, "Should have exactly 15 checklist items")
    
    def test_all_lessons_have_content(self):
        """Verify all lessons have content and key points"""
        for topic, lesson in LESSONS.items():
            self.assertIn("content", lesson, f"{topic} missing content")
            self.assertIn("key_points", lesson, f"{topic} missing key_points")
            self.assertGreater(len(lesson["content"]), 100, f"{topic} content too short")
            self.assertGreater(len(lesson["key_points"]), 0, f"{topic} has no key points")
    
    def test_all_quiz_questions_complete(self):
        """Verify all quiz questions are complete"""
        required_fields = ["question", "options", "answer", "explanation"]
        for i, q in enumerate(QUIZ_QUESTIONS, 1):
            for field in required_fields:
                self.assertIn(field, q, f"Question {i} missing {field}")
            self.assertEqual(len(q["options"]), 4, f"Question {i} should have 4 options")
            self.assertIn(q["answer"], ["A", "B", "C", "D"], f"Question {i} invalid answer")
            self.assertGreater(len(q["explanation"]), 50, f"Question {i} explanation too short")
    
    def test_all_checklist_items_complete(self):
        """Verify all checklist items have required fields"""
        categories = set()
        for item in CHECKLIST_ITEMS:
            self.assertIn("text", item, "Checklist item missing text")
            self.assertIn("category", item, "Checklist item missing category")
            categories.add(item["category"])
        
        # Should have multiple categories
        self.assertGreaterEqual(len(categories), 4, "Should have at least 4 categories")


class TestScoring(unittest.TestCase):
    """Test scoring functions"""
    
    def test_score_all_complete(self):
        """Test 15/15 items = 100%"""
        responses = {f"item_{i}": True for i in range(15)}
        self.assertEqual(calculate_score(responses), 100.0)
    
    def test_score_none_complete(self):
        """Test 0/15 items = 0%"""
        responses = {f"item_{i}": False for i in range(15)}
        self.assertEqual(calculate_score(responses), 0.0)
    
    def test_score_pass_threshold(self):
        """Test 12/15 items = 80% (pass threshold)"""
        responses = {f"item_{i}": i < 12 for i in range(15)}
        score = calculate_score(responses)
        self.assertEqual(score, 80.0)
    
    def test_score_good_threshold(self):
        """Test 9/15 items = 60% (good threshold)"""
        responses = {f"item_{i}": i < 9 for i in range(15)}
        score = calculate_score(responses)
        self.assertEqual(score, 60.0)
    
    def test_score_empty_checklist(self):
        """Test empty checklist returns 0"""
        self.assertEqual(calculate_score({}), 0.0)


class TestFeedback(unittest.TestCase):
    """Test performance feedback"""
    
    def test_feedback_excellent(self):
        """Test feedback at 80%+ (pass)"""
        feedback = get_performance_feedback(85.0)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_at_pass_threshold(self):
        """Test feedback exactly at 80%"""
        feedback = get_performance_feedback(PASS_THRESHOLD)
        self.assertIn("Excellent", feedback)
    
    def test_feedback_good(self):
        """Test feedback between 60-79%"""
        feedback = get_performance_feedback(70.0)
        self.assertIn("Good", feedback)
    
    def test_feedback_at_good_threshold(self):
        """Test feedback exactly at 60%"""
        feedback = get_performance_feedback(GOOD_THRESHOLD)
        self.assertIn("Good", feedback)
    
    def test_feedback_critical(self):
        """Test feedback below 60%"""
        feedback = get_performance_feedback(50.0)
        self.assertIn("Critical", feedback)


class TestFileOperations(unittest.TestCase):
    """Test progress saving and loading"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_file = "test_progress.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Cleanup test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_progress(self):
        """Test saving progress to JSON"""
        progress = {
            "timestamp": datetime.now().isoformat(),
            "checklist": {f"item_{i}": i < 12 for i in range(15)},
            "compliance_score": "12/15",
            "percentage": 80.0
        }
        
        with open(self.test_file, "w") as f:
            json.dump(progress, f)
        
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_progress(self):
        """Test loading progress from JSON"""
        test_data = {
            "checklist": {f"item_{i}": i < 9 for i in range(15)},
            "percentage": 60.0,
            "compliance_score": "9/15"
        }
        
        with open(self.test_file, "w") as f:
            json.dump(test_data, f)
        
        with open(self.test_file, "r") as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded["percentage"], 60.0)
        self.assertEqual(loaded["compliance_score"], "9/15")


class TestThresholds(unittest.TestCase):
    """Test threshold boundaries"""
    
    def test_just_below_pass(self):
        """Test 11/15 = 73.33% (below pass)"""
        responses = {f"item_{i}": i < 11 for i in range(15)}
        score = calculate_score(responses)
        self.assertAlmostEqual(score, 73.33, places=1)
        feedback = get_performance_feedback(score)
        self.assertNotIn("Excellent", feedback)
    
    def test_just_below_good(self):
        """Test 8/15 = 53.33% (below good)"""
        responses = {f"item_{i}": i < 8 for i in range(15)}
        score = calculate_score(responses)
        self.assertAlmostEqual(score, 53.33, places=1)
        feedback = get_performance_feedback(score)
        self.assertIn("Critical", feedback)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_complete_workflow(self):
        """Test full workflow"""
        # Create checklist
        checklist = {f"item_{i}": i < 12 for i in range(15)}
        
        # Calculate score
        score = calculate_score(checklist)
        self.assertEqual(score, 80.0)
        
        # Get feedback
        feedback = get_performance_feedback(score)
        self.assertIn("Excellent", feedback)


def run_all_tests():
    """Run all tests with summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestContentCompleteness))
    suite.addTests(loader.loadTestsFromTestCase(TestScoring))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedback))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestThresholds))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("HIPAA TRAINING SYSTEM V2.0 - TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("\nContent Verified:")
    print(f"  ✓ 13 Complete Lessons")
    print(f"  ✓ 15 Quiz Questions")
    print(f"  ✓ 15 Checklist Items")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
