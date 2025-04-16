    #!/bin/bash
    
    cd codeprojects/txesting/
    source .venv/bin/activate
    cd student_testing/
    python3 manage.py runserver 0.0.0.0:8000 &