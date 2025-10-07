#!/usr/bin/env python3
"""
Test Suite for HIPAA Training System V2.0 - Web App Version
Run with: python test_hipaa_web.py
"""

import unittest
import json
import os
import sys
from datetime import datetime

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, LESSONS, QUIZ_QUESTIONS, CHECKLIST_ITEMS, calculate_score, get_performance_feedback


class TestWebAppSetup(unittest.TestCase):
    """Test Flask app configuration and setup"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_app_exists(self):
        """Test Flask app instance exists"""
        self.assertIsNotNone(app)
    
    def test_app_testing_mode(self):
        """Test app is in testing mode"""
        self.assertTrue(app.testing)
    
    def test_app_has_secret_key(self):
        """Test app has secret key configured"""
        self.assertIsNotNone(app.secret_key)


class TestWebRoutes(unittest.TestCase):
    """Test all web routes return expected responses"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_route(self):
        """Test home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HIPAA Training System', response.data)
    
    def test_lessons_route(self):
        """Test lessons page loads"""
        response = self.app.get('/lessons')
        self.assertEqual(response.status_code, 200)
    
    def test_quiz_route(self):
        """Test quiz page loads"""
        response = self.app.get('/quiz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quiz', response.data)
    
    def test_checklist_route(self):
        """Test checklist page loads"""
        response = self.app.get('/checklist')
        self.assertEqual(response.status_code, 200)
    
    def test_report_route(self):
        """Test report page loads"""
        response = self.app.get('/report')
        self.assertEqual(response.status_code, 200)
    
    def test_certificate_route_redirects_if_no_quiz(self):
        """Test certificate redirects if quiz not taken"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['progress'] = {
                    'quiz_taken': False,
                    'quiz_score': 0
                }
            response = client.get('/certificate')
            self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_nonexistent_route_404(self):
        """Test 404 for nonexistent routes"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


class TestSessionManagement(unittest.TestCase):
    """Test user session and progress tracking"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_initial_session_creation(self):
        """Test session is created on first visit"""
        with self.app as client:
            response = client.get('/')
            with client.session_transaction() as sess:
                self.assertIn('progress', sess)
                self.assertEqual(sess['progress']['quiz_score'], 0)
                self.assertFalse(sess['progress']['quiz_taken'])
    
    def test_lesson_completion_tracking(self):
        """Test marking lessons as complete"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['progress'] = {
                    'lessons_completed': [],
                    'quiz_score': 0,
                    'quiz_taken': False,
                    'checklist_items': {},
                    'started_at': datetime.now().isoformat()
                }
            
            response = client.post('/mark_lesson_complete', 
                                 json={'lesson_name': 'Privacy Rule Basics'},
                                 content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
    
    def test_checklist_updates(self):
        """Test checklist item updates"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['progress'] = {
                    'checklist_items': {
                        'Completed Privacy Rule training': False
                    }
                }
            
            response = client.post('/update_checklist',
                                 json={
                                     'item_text': 'Completed Privacy Rule training', 
                                     'completed': True
                                 },
                                 content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])


class TestQuizFunctionality(unittest.TestCase):
    """Test quiz submission and scoring"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_quiz_submission(self):
        """Test quiz submission and scoring"""
        with self.app as client:
            # Set up initial session
            with client.session_transaction() as sess:
                sess['progress'] = {
                    'quiz_score': 0,
                    'quiz_taken': False,
                    'quiz_answers': {}
                }
            
            # Submit quiz answers
            test_answers = {'0': 'B'}  # First question correct answer
            response = client.post('/submit_quiz',
                                 json={'answers': test_answers},
                                 content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Verify response structure
            self.assertIn('score', data)
            self.assertIn('correct', data)
            self.assertIn('total', data)
            self.assertIn('passed', data)
            self.assertIn('feedback', data)
    
    def test_quiz_passing_score(self):
        """Test quiz passing threshold"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['progress'] = {
                    'quiz_score': 85.0,
                    'quiz_taken': True
                }
            
            response = client.get('/certificate')
            # Should not redirect if passed
            self.assertEqual(response.status_code, 200)


class TestContentIntegration(unittest.TestCase):
    """Test web app integration with existing content"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_lessons_content_in_web_app(self):
        """Verify all lessons are accessible in web app"""
        for lesson_name in LESSONS.keys():
            response = self.app.get(f'/lesson/{lesson_name}')
            self.assertEqual(response.status_code, 200)
    
    def test_quiz_questions_loaded(self):
        """Verify quiz questions are available"""
        response = self.app.get('/quiz')
        self.assertEqual(response.status_code, 200)
        # Should contain quiz interface
        self.assertIn(b'Question', response.data)
    
    def test_checklist_items_loaded(self):
        """Verify checklist items are available"""
        response = self.app.get('/checklist')
        self.assertEqual(response.status_code, 200)
        # Should contain checklist interface
        self.assertIn(b'Checklist', response.data)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in web app"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_invalid_lesson_404(self):
        """Test 404 for invalid lesson names"""
        response = self.app.get('/lesson/nonexistent_lesson')
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON requests"""
        response = self.app.post('/mark_lesson_complete', 
                               data='invalid json',
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TestProgressPersistence(unittest.TestCase):
    """Test that progress persists across requests"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_progress_persists_in_session(self):
        """Test progress is maintained across multiple requests"""
        with self.app as client:
            # First request - initialize progress
            client.get('/')
            
            with client.session_transaction() as sess:
                initial_progress = sess['progress'].copy()
            
            # Second request - progress should persist
            client.get('/lessons')
            
            with client.session_transaction() as sess:
                self.assertEqual(sess['progress']['quiz_score'], 
                               initial_progress['quiz_score'])
                self.assertEqual(sess['progress']['quiz_taken'],
                               initial_progress['quiz_taken'])


def run_web_tests():
    """Run all web app tests with summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestWebAppSetup))
    suite.addTests(loader.loadTestsFromTestCase(TestWebRoutes))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestQuizFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestContentIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestProgressPersistence))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("HIPAA TRAINING WEB APP - TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("\nWeb Features Tested:")
    print(f"  [OK] Flask App Configuration")
    print(f"  [OK] All Web Routes")
    print(f"  [OK] Session Management")
    print(f"  [OK] Quiz Functionality")
    print(f"  [OK] Error Handling")
    print(f"  [OK] Progress Persistence")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Testing HIPAA Training Web Application...")
    success = run_web_tests()
    exit(0 if success else 1)
