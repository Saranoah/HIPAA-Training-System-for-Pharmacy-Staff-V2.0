import pytest
from hipaa_system_v3 import ComplianceDashboard, DatabaseManager
from unittest.mock import Mock, patch
import csv
import json

@pytest.fixture
def dashboard():
    dash = ComplianceDashboard()
    dash.db = Mock()
    return dash

def test_generate_enterprise_report_csv(dashboard):
    """Test CSV report generation"""
    # Mock database responses
    dashboard.db._get_connection.return_value.__enter__.return_value.execute.return_value.fetchone.side_effect = [
        {'total_users': 50, 'avg_score': 85.5, 'pass_rate': 90.0},
        {'total_certs': 45, 'active_certs': 40, 'expired_certs': 5}
    ]
    
    with patch('builtins.open', create=True) as mock_file:
        filename = dashboard.generate_enterprise_report('csv')
        assert filename.startswith('compliance_dashboard_')
        assert filename.endswith('.csv')

def test_generate_enterprise_report_json(dashboard):
    """Test JSON report generation"""
    dashboard.db._get_connection.return_value.__enter__.return_value.execute.return_value.fetchone.side_effect = [
        {'total_users': 50, 'avg_score': 85.5, 'pass_rate': 90.0},
        {'total_certs': 45, 'active_certs': 40, 'expired_certs': 5}
    ]
    
    with patch('builtins.open', create=True):
        filename = dashboard.generate_enterprise_report('json')
        assert filename.startswith('compliance_dashboard_')
        assert filename.endswith('.json')
