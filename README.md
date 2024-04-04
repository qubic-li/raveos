# Qubic RaveOs Miner
This is the integration of the main client from qubic.li to RaveOs.

Qubminer are now successfully integrated into RaveOS.

***No fees. Absolutely - FREE.***

![Qubminer](/img/Header.png)

## Qubic Resources

- [Qubic Website](https://web.qubic.li/)
- [Qubic Web Wallet](https://wallet.qubic.li/)
- [Qubic Mining Pool](https://app.qubic.li/public/)
- [Official Qubic Client](https://github.com/qubic-li/client?tab=readme-ov-file#download)

## :warning: RaveOs Mandatory Installation Instructions
- The CPU where you run the Client must support AVX2 or AVX512 CPU instructions
`cat /proc/cpuinfo | grep avx2`(check if `avx2` is in the result)
- Cuda 12+ drivers (535+)
`upgrade 8926-2226` (or newer)
- RAM >= 16Go improves CPU it/s
- Higher RAM frequencies improves CPU it/s
- Do not overload your CPUs with threads, instead, aim to find the sweetpoint

*Only NVIDIA GPU compatible*
<br>

## Configuration
The startup script takes values from the flight sheet to complete the default configuration (`appsettings_global.json`).

There are a lot of necessary libraries for work into syslib folder

Each time the miner starts, the `appsettings.json` file is recreated

### The main settings:
![Flight Sheet](/img/FlightSheet.png)

### GPU+CPU (Dual) mining:
![Flight Sheet Dual](/img/FlightSheetDual.png)
<br>
Extra config arguments exemple:
```
"accessToken":"YOUROWNTOKEN"
"amountOfThreads":4
```

### GPU mining:
![Flight Sheet GPU](/img/FlightSheetGPU.png)
<br>
Extra config arguments exemple:
```
"accessToken":"YOUROWNTOKEN"
```

### CPU mining:
![Flight Sheet CPU](/img/FlightSheetCPU.png)
<br>
Extra config arguments exemple:
```
"cpuOnly":"yes"
"amountOfThreads":24
"accessToken":"YOUROWNTOKEN"
```

### Recommended RaveOS GPU overclocks :  

Please use "Tunning Settings" from workers's dashboard to set global or specific OC:

**Medium**  
3000 series ```nvidia-smi -lmc 7000 && nvidia-smi -lgc 1500```  
4000 series ```nvidia-smi -lmc 7000 && nvidia-smi -lgc 2400```  
**High**  
3000 series ```nvidia-smi -lmc 7000 && nvidia-smi -lgc 1700```  
4000 series ```nvidia-smi -lmc 7000 && nvidia-smi -lgc 2900```  


### Extra config arguments Box (options):

| Setting | Description                                                                                                                                                                                                                                  |
| ---- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```"accessToken":``` | This is you personal JWT Token which you can obtain from the Control Panel at qubic.li                                                                                                                                                       |
| ```"payoutId":``` | This is the ID you want to get token payout for your found solutions.                                                                                                                                                                        |
| ```"hugePages":nnnn``` | Depending on your environment you might want to enable huge pages. This can increase your iterations per second. The trainer will tell you what is the optimal setting when it detects a wrong value. The number depends on the number of threads: nb_threads * 52 (e.g., 16 * 52 = 832). If trainer is unstable please remove. |
|  ```"overwrites": {"AVX512": false}``` | Disable AVX512 and enforce AVX2 (AVX Intel CPU not working)                                                                                                                                                                                  |
| ```"overwrites": {"SKYLAKE": true}```  | Enforce SKYLAKE (AVX Intel CPU not working)                                                                                                                                                                                                  |
<br>
