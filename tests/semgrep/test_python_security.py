# Tests for custom Semgrep Python security rules defined in .semgrep.yml
#
# Semgrep test format:
#   # ruleid: <rule-id>   → next non-comment line MUST match the rule (true positive)
#   # ok: <rule-id>       → next non-comment line MUST NOT match the rule (true negative)
#
# Run:  semgrep --test --config .semgrep.yml tests/semgrep/test_python_security.py

import ast
import hashlib
import json
import pickle
import secrets
import subprocess
import sqlite3
import yaml


# ---------------------------------------------------------------------------
# python.no-eval-or-exec
# ---------------------------------------------------------------------------

# ruleid: python.no-eval-or-exec
eval("1 + 1")

# ruleid: python.no-eval-or-exec
exec("print('hello')")

# ok: python.no-eval-or-exec
ast.literal_eval("{'key': 'value'}")

# ok: python.no-eval-or-exec
result = compile("1 + 1", "<string>", "eval")


# ---------------------------------------------------------------------------
# python.no-pickle-deserialization
# ---------------------------------------------------------------------------

def deserialize_untrusted(data):
    # ruleid: python.no-pickle-deserialization
    return pickle.loads(data)


def deserialize_from_file(f):
    # ruleid: python.no-pickle-deserialization
    return pickle.load(f)


def deserialize_safe(data: str):
    # ok: python.no-pickle-deserialization
    return json.loads(data)


def serialize_only(obj):
    # ok: python.no-pickle-deserialization
    # Serialization (pickle.dumps/dump) is allowed — only loading is dangerous
    return pickle.dumps(obj)


# ---------------------------------------------------------------------------
# python.yaml-load-requires-safe-loader
# ---------------------------------------------------------------------------

def parse_config_unsafe(stream):
    # ruleid: python.yaml-load-requires-safe-loader
    return yaml.load(stream)


def parse_config_safe(stream):
    # ok: python.yaml-load-requires-safe-loader
    return yaml.safe_load(stream)


def parse_config_explicit_loader(stream):
    # ok: python.yaml-load-requires-safe-loader
    return yaml.load(stream, Loader=yaml.SafeLoader)


# ---------------------------------------------------------------------------
# python.subprocess-shell-true
# ---------------------------------------------------------------------------

def run_command_unsafe(user_input):
    # ruleid: python.subprocess-shell-true
    subprocess.run(user_input, shell=True)


def run_command_call_unsafe(cmd):
    # ruleid: python.subprocess-shell-true
    subprocess.call(cmd, shell=True)


def check_call_unsafe(cmd):
    # ruleid: python.subprocess-shell-true
    subprocess.check_call(cmd, shell=True)


def check_output_unsafe(cmd):
    # ruleid: python.subprocess-shell-true
    subprocess.check_output(cmd, shell=True)


def popen_unsafe(cmd):
    # ruleid: python.subprocess-shell-true
    subprocess.Popen(cmd, shell=True)


def run_command_safe(cmd: list):
    # ok: python.subprocess-shell-true
    subprocess.run(cmd, shell=False)


def run_command_default(cmd: list):
    # ok: python.subprocess-shell-true
    # shell defaults to False
    subprocess.run(cmd)


# ---------------------------------------------------------------------------
# python.sql-string-concat-in-execute
# ---------------------------------------------------------------------------

def fetch_user_by_name_unsafe(conn, username: str):
    cursor = conn.cursor()
    # ruleid: python.sql-string-concat-in-execute
    cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")


def fetch_user_fstring_unsafe(conn, user_id: int):
    cursor = conn.cursor()
    # ruleid: python.sql-string-concat-in-execute
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")


def fetch_user_format_unsafe(conn, role: str):
    cursor = conn.cursor()
    # ruleid: python.sql-string-concat-in-execute
    cursor.execute("SELECT * FROM users WHERE role = '%s'" % role)


def fetch_user_format_method_unsafe(conn, status: str):
    cursor = conn.cursor()
    # ruleid: python.sql-string-concat-in-execute
    cursor.execute("SELECT * FROM users WHERE status = '{}'".format(status))


def fetch_user_safe(conn, username: str):
    cursor = conn.cursor()
    # ok: python.sql-string-concat-in-execute
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))


def fetch_user_named_param_safe(conn, username: str):
    cursor = conn.cursor()
    # ok: python.sql-string-concat-in-execute
    cursor.execute("SELECT * FROM users WHERE name = :name", {"name": username})
