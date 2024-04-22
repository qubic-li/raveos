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

<br>

> [!NOTE]
> The defualt configuration is vor NVIDIA. To enable AMD GPU you need to add `"trainer":{"gpuVersion":"AMD"}` to Extra config arguments.

> [!IMPORTANT]
> AMD Version is currently only allowed in `qubic.li CPU/GPU Mining (Fixed Reward 85%)`


## Configuration
The startup script takes values from the flight sheet to complete the default configuration (`appsettings_global.json`).

There are a lot of necessary libraries for work into syslib folder

Each time the miner starts, the `appsettings.json` file is recreated

> [!IMPORTANT]
> For CPU you have to define which Version should be used. The `cpuVersion` propery can be used. Please refer to https://github.com/qubic-li/client/?tab=readme-ov-file#qli-trainer-options for a list of available versions. You can also find there all other available options.

### The main settings:
![Flight Sheet](/img/FlightSheet.png)

### GPU+CPU (Dual) mining:
![Flight Sheet Dual](/img/FlightSheetDual.png)
<br>
Extra config arguments exemple:
```
"accessToken":"YOUROWNTOKEN"
"trainer":{"cpuThreads":4}
```

**Sample Configuration for AMD GPU's + CPU dual mining**
```
"accessToken":"YOUROWNTOKEN"
"trainer":{"gpuVersion":"AMD","cpuThreads":4}
```

### GPU mining:
![Flight Sheet GPU](/img/FlightSheetGPU.png)
<br>
Extra config arguments exemple:
```
"accessToken":"YOUROWNTOKEN"
"trainer":{"cpu":"false"}
```

**Sample Configuration for AMD GPU's**
```
"accessToken":"YOUROWNTOKEN"
"trainer":{"cpu":"false","gpuVersion":"AMD"}
```

### CPU mining:
![Flight Sheet CPU](/img/FlightSheetCPU.png)
<br>
Extra config arguments exemple:
```
"accessToken":"YOUROWNTOKEN"
"trainer":{"cpu":"true","gpu":"false","cpuThreads":4}
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
| ```"hugePages":nnnn``` | Depending on your environment you might want to enable huge pages. This can increase your iterations per second. The trainer will tell you what is the optimal setting when it detects a wrong value. The number depends on the number of threads: nb_threads * 52 (e.g., 16 * 52 = 832). If trainer is unstable please remove.|
| ```"trainer": {}```  | The trainer configuration options                                                                                                                                                                                                 |

<br>

### Trainer Options

```json
{
	"cpu":false,
	"cpuVersion":"AVX512",
	"cpuThreads":16,
	"cpuAffinity":"",
	"cpuVariant":"",
	"gpu":true,
	"gpuVersion":"CUDA12",
	"gpuCards":"",
	"gpuVariant":""
}
```

|  Setting 	|  Default Value 	|  Description 	|
|---	|---	|---	|
|  *cpu 	|  false	|  Enable CPU Training	|
|  *gpu 	|  false	|  Enable GPU Training	|
|  cpuVersion 	|  "GENERIC"	|  CPU Version to be used [QLI Trainer Options](#qli-trainer-options)	|
|  gpuVersion 	|  null	|  GPU Version to be used [QLI Trainer Options](#qli-trainer-options)	|
|  cpuThreads 	|  1	|  Number of Threads used for CPU training	|
|  gpuCards 	|  null	|  Which GPU Cards should be used (see details below; available from client `>=1.9.5` and runner `>=105.3`)	|
|  cpuAffinity	|  null	|  CPU Affinity for CPU training	|
|  cpuVariant 	|  null	|  Which Variant of CPU trainer should be used	|
|  gpuVariant 	|  null	|  Which Variant of GPU trainer should be used	|

> [!NOTE]
> The `gpuCards` property can be used to select `gThreads`. The default configuration is `auto tune` for all cards.<br>
> For each GPU you can use (comma separated):<br>
> `-1` => auto tune<br>
>  `0` => disable GPU<br>
> `>0` => number of `gThreads` to be used<br>
> >e.g.: `0,-1,-1,-1,-1,-1` => GPU#1 disabled, #1-5 auto tuen<br>
> e.g.: `0` => GPU#0 disabled, if there are more, all will be auto tuned<br>
> e.g.: `512,256,256,256,256,512` => set `gThread` to 512 on GPU#0 and GPU#5, 256 to the rest<br>