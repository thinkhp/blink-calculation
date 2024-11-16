build_mac:
	rm -rf build dist
	pyinstaller --clean blink_calculation_mac.spec

build_debug:
	rm -rf build dist
	pyinstaller --clean blink_calculation.spec
