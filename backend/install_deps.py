import subprocess
import sys

def install_dependencies():
    print("开始安装依赖...")
    
    # 1. 首先安装最新版本的onnxruntime（从错误信息看，1.15.1不可用）
    subprocess.check_call([sys.executable, "-m", "pip", "install", "onnxruntime==1.17.0"])
    print("已安装onnxruntime 1.17.0")
    
    # 2. 安装基础依赖，但排除特定包
    dependencies = [
        "fastapi==0.104.1",
        "uvicorn==0.23.2",
        "pydantic==2.4.2",
        "python-multipart==0.0.6",
        "pymupdf==1.23.5",
        "celery==5.3.4",
        "redis==5.0.1",
        "python-dotenv==1.0.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "httpx==0.25.1",
        "langchain==0.0.267",
        "langchain-text-splitters"
    ]
    
    for dep in dependencies:
        print(f"安装: {dep}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
    # 3. 单独安装需要特别处理的包
    try:
        print("安装 chromadb...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chromadb==0.4.18"])
    except subprocess.CalledProcessError:
        print("尝试安装最新版 chromadb...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chromadb"])
    
    try:
        print("安装 sentence-transformers...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers==2.2.2"])
    except subprocess.CalledProcessError:
        print("尝试安装最新版 sentence-transformers...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers"])
    
    # 4. 单独安装unstructured和它的依赖
    print("安装 unstructured 基础版本...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "unstructured==0.10.30"])
    
    # 5. 安装文档处理依赖
    print("安装文档处理依赖...")
    doc_dependencies = [
        "markdown",
        "pdf2image",
        "pypdf",
        "pdfminer.six",
        "python-docx"
    ]
    
    for dep in doc_dependencies:
        print(f"安装: {dep}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except:
            print(f"警告: 安装 {dep} 失败，但仍将继续")
    
    print("所有依赖安装完成!")

if __name__ == "__main__":
    install_dependencies() 