import torch.cuda

def test_check_cuda_status():
    try:
        assert torch.cuda.is_available()
        print("CUDA is available. GPU can be used.")
    except AssertionError:
        print("CUDA is not available. GPU cannot be used.")
    except Exception as e:
        print(f"An error occurred while checking CUDA status: {e}")