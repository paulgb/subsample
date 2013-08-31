
TEST_OUTPUT_DIR=tests/test_output
export FIXTURES_DIR=tests/fixtures
TEST_CASES_DIR=tests/test_cases
TEST_EXPECTATIONS_DIR=tests/test_expectations

test : test_reservoir test_twopass test_approximate

.SECONDARY :
.SILENT :

$(TEST_OUTPUT_DIR) : subsample/*.py
	rm -rf $(TEST_OUTPUT_DIR)
	mkdir -p $(TEST_OUTPUT_DIR)


fixture_data : $(FIXTURES_DIR)/data.csv


$(FIXTURES_DIR)/data.csv : subsample/*.py
	mkdir -p $(FIXTURES_DIR)
	python util/gensource.py -n 10000 > $(FIXTURES_DIR)/data.csv


test_% : $(TEST_OUTPUT_DIR)/test_%.out $(TEST_EXPECTATIONS_DIR)/test_%.out
	if diff $^; then \
		echo "Test $* Passed"; \
	else \
		echo "Test $* Failed"; \
	fi


$(TEST_OUTPUT_DIR)/test_%.out : $(TEST_CASES_DIR)/test_%.sh fixture_data $(TEST_OUTPUT_DIR)
	bash $< > $@


# Uncomment this to generate expectation data from new test cases
#$(TEST_EXPECTATIONS_DIR)/test_%.out : $(TEST_CASES_DIR)/test_%.sh
#	mkdir -p $(TEST_EXPECTATIONS_DIR)
#	echo "Warning: no expectation for $* found; generating"
#	bash $< > $@



