# Experiments in Compression

After listening to the CoRecursive podcast [interviewing](https://corecursive.com/data-compression-yann-collet) Yann Collet, the author of [LZ4](https://github.com/lz4/lz4) and [zstd](http://facebook.github.io/zstd/), I was curious as to how compression could improve transmission time for firmware updates over low bandwith links.

The situation is:

1. firmware binaries in the 10kB-1MB range
2. transmission link is _very_ slow, eg 19200 baud, < 2 kB/s
3. comms must be the bottleneck: decompressor speed + flash write speed should not add any extra delay
4. relative to the data size, unlimited compressor resources
5. decompressor code size needs to fit in a bootloader, somewhere around the 5kB mark perhaps (although in initial hand-waving, will disregard this constraint in favour of seeing what the maximum theoretical compression should be)

First run with LZ4 and zstd, on a representative firmware binary (there are ~10 in the final system):

```bash
% lz4 --best ../build-stm32/sample_firmware.bin
Compressed 24704 bytes into 19378 bytes ==> 78.44%

% zstd --ultra ../build-stm32/sample_firmware.bin
../build-stm32/sample_firmware.bin : 68.58%   (  41.2 KiB =>   28.3 KiB, ../build-stm32/sample_firmware.bin.zst) 
```

So ~20% savings with lz4 and ~30% with zstd.

What about with a dictionary ith dictionary:

```bash
% find ../build-stm32 -name "*.bin" > firmware_binaries.lst

% zstd --train -o firmware.dict $(cat firmware_binaries.lst)

% zstd --train -o firmware.dict --maxdict= $(cat firmware_binaries.lst)
p
% zstd --ultra -D firmware.dict ../build-stm32/pullkey/pullkey-biscuit462-qspy-bootloaded.bin -o compress-test/pullkey-biscuit462-qspy-bootloaded.bin.zstd

```


% lz4 --best -D firmware.dict ../build-stm32representative_firmware.bin

(venv) josh@Joshs-MacBook firmware % lz4 --best -D firmware.dict  ../build-stm32/pullkey/pullkey-biscuit462-noqspy-bootloaded.bin compress-test/pullkey-biscuit462-noqspy-bootloaded.bin.dict.lz4
Compressed 24704 bytes into 17911 bytes ==> 72.50%
```



## Link dump

### Dictionaries
https://blog.cloudflare.com/improving-compression-with-preset-deflate-dictionary/
http://fastcompression.blogspot.com/2018/02/when-to-use-dictionary-compression.html
https://github.com/lz4/lz4/issues/559
