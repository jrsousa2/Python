import torch

print(torch.cuda.is_available())  # Should return True if CUDA is enabled
print(torch.cuda.device_count())  # Should return the number of available GPUs
print(torch.cuda.get_device_name(0))  # Should print the name of GPU 1 if it's available

# MAIS UM TESTE
print(torch.rand(2,3).cuda())
