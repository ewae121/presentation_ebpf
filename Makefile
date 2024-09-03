PRESENTATION_NAME = ebpf_presentation
SRC = $(PRESENTATION_NAME).md

BIN_DIR = bin
MARP_URL = https://github.com/marp-team/marp-cli/releases/download/v3.4.0/marp-cli-v3.4.0-linux.tar.gz
MARP_FILENAME = $(shell basename $(MARP_URL))
MARP_APP = $(BIN_DIR)/marp

BUILD_DIR = build

all: check-marp clean build

build: build-init build-html
build-html: build-init
	cp -r images $(BUILD_DIR)
	./$(MARP_APP) --output $(BUILD_DIR)/$(PRESENTATION_NAME).html $(PRESENTATION_NAME).md
build-init:
	[ -e $(BUILD_DIR) ] || mkdir -p $(BUILD_DIR)

clean-all: clean clean-marp
clean:
	rm -rf $(BUILD_DIR)
clean-marp:
	rm -rf $(BIN_DIR)

check-marp:
	[ ! -e $(MARP_APP) ] || echo "Marp is not installed. If you want to reinstall, run 'make clean-marp'"

install: install-marp
install-marp: clean-marp
	mkdir -p $(BIN_DIR)
	wget --show-progress -O $(BIN_DIR)/$(MARP_FILENAME) $(MARP_URL)
	tar -xzf $(BIN_DIR)/$(MARP_FILENAME) -C $(BIN_DIR)
	