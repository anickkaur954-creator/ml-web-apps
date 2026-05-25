# MNIST 项目 - 本地运行指南

## 📋 运行步骤

### 步骤 1: 等待模型训练完成
模型训练已在后台启动，预计 **5-10 分钟** 完成。

查看训练进度：
```bash
cd backend
tail -f training.log
```

等待看到类似的完成信息：
```
✅ Model saved to: ./models/mnist_model.pkl
   File size: XX.XX MB
```

### 步骤 2: 启动 FastAPI 后端

**打开终端 #1**，运行：
```bash
cd mnist-project/backend
pip install -r requirements.txt  # 如果尚未安装
uvicorn app:app --reload --port 8000
```

你应该看到：
```
Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
INFO:     Model loaded successfully from ../models/mnist_model.pkl
```

### 步骤 3: 启动 Streamlit 前端

**打开终端 #2**，运行：
```bash
cd mnist-project/frontend
pip install -r requirements.txt  # 如果尚未安装
streamlit run streamlit_app.py --server.port 8501
```

你应该看到：
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 步骤 4: 在浏览器中打开应用

访问：**http://localhost:8501**

## 🎨 使用应用

1. **在画布上绘制数字** (0-9)
   - 使用鼠标或触控笔在白色画布上绘制
   - 尽量让数字填满画布

2. **点击 "🎯 Predict" 按钮**
   - 应用会将图像发送到后端
   - 后端使用CNN模型进行预测

3. **查看预测结果**
   - 显示识别的数字（0-9）
   - 显示置信度百分比
   - 显示所有数字的概率条形图

4. **清除画布**
   - 点击 "🗑️ Clear Canvas" 重新开始

## 🔍 API 测试

### 测试后端健康检查
```bash
curl http://localhost:8000/
```

### 测试预测端点
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAA..."}'
```

## 🛠️ 故障排除

### 问题：端口已在使用
```bash
# 查看占用8000端口的进程
lsof -i :8000

# 终止进程
kill -9 <PID>
```

### 问题：模型文件未找到
确保模型训练完成：
```bash
ls -lh mnist-project/models/mnist_model.pkl
```

如果不存在，运行：
```bash
cd mnist-project/backend
python train_model.py
```

### 问题：导入错误 (streamlit_drawable_canvas)
```bash
cd mnist-project/frontend
pip install streamlit-drawable-canvas==0.9.3
```

### 问题：连接被拒绝
确保后端正在运行 (http://localhost:8000)

## 📊 模型信息

- **架构**: CNN (Convolutional Neural Network)
- **输入**: 28x28 灰度图像
- **输出**: 10 个数字 (0-9) 的概率
- **训练集**: MNIST 60,000 张图像
- **验证准确率**: ~98%
- **测试准确率**: ~97%

## 🔗 快速链接

- **Streamlit 应用**: http://localhost:8501
- **FastAPI 文档**: http://localhost:8000/docs
- **FastAPI 重新文档**: http://localhost:8000/redoc

## 📝 常用命令

```bash
# 查看训练日志
tail -f backend/training.log

# 列出模型文件
ls -lh mnist-project/models/

# 测试后端
curl http://localhost:8000/health

# 重新启动后端
# 先在终端中按 Ctrl+C，然后重新运行 uvicorn 命令

# 重新启动前端
# 先在终端中按 Ctrl+C，然后重新运行 streamlit 命令
```

## ✅ 检查清单

- [ ] 模型训练完成 (`mnist_model.pkl` 存在)
- [ ] 后端运行在 http://localhost:8000
- [ ] 前端运行在 http://localhost:8501
- [ ] 可以访问 http://localhost:8501
- [ ] 可以在画布上绘制
- [ ] 预测功能正常工作
- [ ] 显示正确的预测结果

---

**祝使用愉快！** 🚀

如有问题，请检查日志文件或终端输出获取更多信息。
