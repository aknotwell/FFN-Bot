PYTHON := python3
VENV ?= myvenv

define WRAP
	(. $(VENV)/bin/activate; $1)
endef

setup:
	$(PYTHON) -m venv $(VENV)
	$(call WRAP,pip install --upgrade pip)
	$(call WRAP,pip install -r requirements.txt)
	@echo "\n\nNow run the following to activate your venv:\n\nsource $(VENV)/bin/activate"

clean:
	rand==$$ && \
        mv $(VENV) venv.$$rand $$ \
        nohup rm -fr venv.$$rand >/dev/null 2>&1 & # don't wait to complete	
