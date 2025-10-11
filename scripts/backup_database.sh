#!/bin/bash

# HIPAA Training System - Database Backup Script
BACKUP_DIR="backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_PATH="data/hipaa_training.db"

echo "💾 Starting HIPAA Training System backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup SQLite database
if [[ -f "$DB_PATH" ]]; then
    echo "📊 Backing up SQLite database..."
    sqlite3 $DB_PATH ".backup $BACKUP_DIR/hipaa_training_$TIMESTAMP.db"
    
    # Compress backup
    gzip $BACKUP_DIR/hipaa_training_$TIMESTAMP.db
    echo "✓ Database backed up to: $BACKUP_DIR/hipaa_training_$TIMESTAMP.db.gz"
else
    echo "⚠️ Database file $DB_PATH not found."
fi

# Backup content files
echo "📝 Backing up content files..."
tar -czf $BACKUP_DIR/content_$TIMESTAMP.tar.gz content/

# Backup audit logs
if [[ -f "hipaa_audit.log" ]]; then
    echo "📋 Backing up audit logs..."
    cp hipaa_audit.log $BACKUP_DIR/hipaa_audit_$TIMESTAMP.log
fi

# Clean up old backups (keep last 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.log" -mtime +30 -delete

echo "✅ Backup completed successfully!"
echo "📁 Backup location: $BACKUP_DIR/"
