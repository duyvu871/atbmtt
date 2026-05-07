.PHONY: help install train live data build_nb notebook clean

help:
	@echo "=========================================================================="
	@echo "🔥 CÁC LỆNH MAKE NHANH CHO PROJECT PHÁT HIỆN RÒ RỈ DỮ LIỆU (ML)"
	@echo "=========================================================================="
	@echo "  make install  - Cài đặt/Đồng bộ môi trường bằng uv"
	@echo "  make train    - Chạy toàn bộ luồng huấn luyện (sinh data -> train -> đánh giá)"
	@echo "  make live     - Chạy kịch bản Demo Live bắt log thời gian thực (SOC Console)"
	@echo "  make data     - Chỉ chạy mô-đun sinh lại dữ liệu mạng (network_logs.csv)"
	@echo "  make build_nb - Dựng lại file demo_notebook.ipynb từ source"
	@echo "  make notebook - Dựng lại Notebook & Mở Jupyter Notebook trên trình duyệt"
	@echo "  make clean    - Dọn dẹp dữ liệu, mô hình, biểu đồ cũ và cache"
	@echo "=========================================================================="

install:
	uv sync

train:
	uv run python run_demo.py

live:
	uv run python live_demo.py

data:
	uv run python src/generate_data.py

build_nb:
	uv run python create_notebook.py

notebook: build_nb
	uv run jupyter notebook demo_notebook.ipynb

clean:
	rm -rf outputs/*.png outputs/*.pkl
	rm -rf data/*.csv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Đã dọn dẹp sạch sẽ thư mục."
