# Builds and runs the C++ tests and demos.
#   make test    -> compile and run every test_*.cpp
#   make demos   -> compile every main.cpp into build/
CXX      ?= g++
CXXFLAGS ?= -std=c++14 -Wall -Wextra -pedantic -O2 -Icommon

CPP_DIRS := 01-recursion 02-searching-sorting 03-algorithm-analysis 04-dynamic-programming
TESTS    := $(foreach d,$(CPP_DIRS),$(wildcard $(d)/test_*.cpp))
TEST_BIN := $(patsubst %.cpp,build/%,$(TESTS))
DEMOS    := $(foreach d,$(CPP_DIRS),$(wildcard $(d)/*_main.cpp))
DEMO_BIN := $(patsubst %.cpp,build/%,$(DEMOS))

.PHONY: test demos clean
test: $(TEST_BIN)
	@set -e; for t in $(TEST_BIN); do echo "== $$t"; ./$$t; done

demos: $(DEMO_BIN)

build/%: %.cpp $(wildcard */*.hpp) common/check.hpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -rf build
