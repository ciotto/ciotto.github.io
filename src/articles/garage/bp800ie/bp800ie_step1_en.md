# BP800 i.e.: How to Build a Tractor with a DIY Twin-Cylinder Fuel-Injected Engine

## Introduction

My passion for engines and electronics found its natural outlet in 2015 when I started getting into amateur *Coltivatori Pulling* competitions—essentially Garden Pulling. It all began by helping a friend build his pulling tractor, but as much as I enjoyed helping him, building your own machine is a whole different story.

Thanks to the woman who would later become my wife, in 2017 I started building my first *cyberpunk*-style tractor. Using a wheelbarrow as a seat, I tried to squeeze all available power out of the kerosene-powered **Lombardini LAP490** engine, sending it to the ground through a **Pasquali 930** gearbox weighted down with **320 kg** of concrete and a chassis designed specifically to pull the weighted sled. In our very first race, we managed to secure first place right away.

Over the years, I improved its appearance and replaced pure gasoline with a mix of gasoline and kerosene, which is much better suited to the compression ratios of an engine designed for kerosene. Later, I also added a board capable of remote starting, purely for the fun of it.

In 2018, I soldered a **Speeduino** ECU with the intention of converting it to fuel injection, but following the principle of *"if it ain't broke, don't fix it,"* I ultimately never finished the upgrade.

---

## The BP800 i.e. Project

A year ago, chatting with my cousin—who has built two tractors himself—we remembered having two **Lombardini LA400** engines in the garage. Over a few beers, the idea was born to build a machine more ambitious than any before: powered by a twin **LA400 converted to fuel injection**.

We immediately divided the tasks clearly: my cousin would mainly handle the frame and bodywork, while I would focus primarily on engine development.

The goal was to build, as far as possible, an unprecedented twin-cylinder engine. After completely overhauling both units, we chose to join them in-line by connecting the PTO-side shaft of one engine to the flywheel-side shaft of the other with a 360° firing order. Since the LA400 has an extremely heavy flywheel, we decided to remove it completely, creating two custom hubs with flanges and a tapered attachment.

Using a hacksaw and file, we manually carved out the channels to accommodate the set screws, which were crucial for ensuring shaft synchronization. Once the flanges were secured and both engines brought to Top Dead Center, we applied a couple of temporary tack welds to maintain perfect alignment while drilling the eight 8 mm holes required to join the two shafts. With the holes drilled, we removed the temporary welds and installed 8 silent blocks to connect the shafts.

With the shafts connected, we moved on to the structure for joining the two engine blocks. We utilized the 4 side holes and 4 bottom holes on each engine, drilling matching holes into two 80x6 mm steel flat bars, and then joined them from below using an extremely robust C-channel profile.

---

## EFI Conversion: Sensors and Actuators on Speeduino

Once the single block was completed, we began working on the electronic fuel injection conversion. The Speeduino ECU requires a series of sensors and actuators to manage fueling and ignition, but the most important is undoubtedly the crankshaft position sensor.

To read RPM, simply knowing the rotational speed is not enough: the ECU must precisely determine the angular position of the shaft to know where the piston is. To do this, a trigger wheel with a missing tooth is typically used.
I therefore created a new flanged hub onto which we mounted a 48-tooth gear, flattening the tooth tips on the lathe.

Initially, I tested some **Hall effect** sensors with digital output (since Speeduino requires a digital signal), but unfortunately they could not handle high frequencies: at 5000 RPM with 48 teeth, we are talking about roughly 4 kHz.

**VR sensors**, on the other hand, generate alternating current and would have required an additional signal conditioner circuit, so I preferred to opt for an optical sensor.

I modified an **IR proximity sensor** by 3D-printing a custom mount to position the receiver in front of the emitter LED, letting the teeth of the gear pass through the middle.

Since LA400 engines are air-cooled, it was impossible to use a classic coolant temperature sensor. I solved this by using two **NTC thermistors** with a B3950 curve, mounted on M10 washers and pinched under the sheet metal that channels air over the cylinder head. By wiring them together, the ECU reads the lowest resistance, which corresponds to the higher temperature between the two cylinder heads.

For fueling, the simplest way to convert a twin-cylinder to injection is using a **Single Point Injection** (SPI) system. We sourced a complete throttle body from a **Fiat Fire** engine, which already integrates the injector, pressure regulator, intake air temperature sensor, TPS, and idle stepper motor.

We positioned the throttle body exactly centered between the two engines so we could build an intake manifold with identical tube lengths, minimizing differences in intake.

For the fuel supply, we mounted a 125 PSI CarBole fuel pump and an external pressure regulator; for now, however, we only use the external regulator as a pressure gauge, relying on the original regulator integrated into the throttle body for actual regulation.

Finally, for ignition, it must be noted that Speeduino cannot directly drive a high-voltage coil. We therefore chose two NGK U5002 coils with built-in ignition modules and spark plug boots, which simply require a digital signal to fire the spark. Finding the electrical documentation wasn't easy, but we eventually figured out the correct wiring.

By choosing a *wasted spark* setup like in the original engine, we were able to drive both coils using a single ECU output.

---

## Software Configuration and Bench Testing

With the initial hardware setup completed, we moved on to the ECU software configuration. We loaded the latest firmware version and, using TunerStudio, set up the *Engine Constants* and *Trigger Settings*, calibrated the temperature sensors with their respective curves, and tested the injector flow rate at different voltages.

During these early tests, an offset appeared on the battery voltage sensor read by the ECU: to fix it, we applied a correction directly in the firmware source code and then flashed a custom version onto the ECU.

With that solved, we bench-tested all sensors and actuators, verifying that the electronics responded properly.

---

## Startup, Mechanical Issues, and a Race Against Time

Since this was the fourth tractor we had prepared, we had a pretty clear idea about starting it: we would use the **dynastart from an Ape TM703** that we had used in the past. However, we weren't sure if it had enough power to turn over a twin-cylinder engine.

We 3D-printed a 22 cm test pulley, but the required effort was too much, making it necessary to enlarge it to 29 cm. To fit the new pulley, we had to modify the lower frame joining the engines: we took the opportunity to redesign it in two sections connected by 6 M8 bolts, making it much easier to separate the two engine blocks.

Once everything was reassembled, we rebuilt the electrical system from scratch. The biggest challenge was finding the original connectors for the Fire throttle body. Furthermore, on the ECU, I had unfortunately used a 2x20 PIN connector similar to old **PC IDE cables**, which is very difficult to crimp without the proper flat cable. We adapted an existing cable, soldering the tiny internal wires onto the larger gauge wires of the harness.

When it came time for the first start attempts, the problems began. The test pulley 3D-printed in 4 pieces caught on the frame and literally shattered into a thousand pieces. We immediately redesigned it and made it as a single piece of PVC, turned from solid stock.

With the first snag resolved, the 8 silent blocks connecting the engine shafts sheared off. We knew this was a critical point, but we hoped it would hold out longer. We replaced them with 8 class 8.8 M8 through-bolts, inserting a 3D-printed spacer whose sole purpose was to allow a tiny degree of freedom between the two flanges.

Having overcome the mechanical breakdowns, the engine still wouldn't start. We checked the TDC timing using a timing light—a complex operation because manually measuring the degrees of advance or retard to correct the optical sensor positioning requires high precision to ensure the ECU calculates injection based on the real shaft position.

Even though the timing seemed correct, the engine would attempt to fire up but die immediately. During these attempts, the computer kept disconnecting from the ECU, the idle stepper motor driver burned out, and the air-fuel mixture was consistently too rich.

With only 4 days left before the race and no time for bench testing, we decided to mount the engine onto the tractor as-is, hoping that full assembly would help us figure out what was wrong. Looking at the system from this new perspective, we noticed that the injector was sometimes sticking open and other times not spraying at all. Suspicion immediately fell on electromagnetic interference. We replaced the original B7HS spark plugs with BR7HS resistor plugs, and finally, the engine started running.

There were two days left until the race. The engine wouldn't idle because a second stepper motor driver had burned out, but we hoped it was just a matter of fine-tuning the maps. We spent the entire last day tweaking maps and testing various wiring changes, but the best result was only decent idle stability.

When clutch drag issues also emerged in the coupling with the chassis, we made the final call: go to the race with our old tractors and bring the new **BP800 i.e.** purely for display.

The interest and curiosity shown by the crowd during the event were immense, giving us a huge boost to continue development.

---

## Problem Analysis and Future Steps

After extensive testing, we concluded that a series of electrical design flaws led to severe instability in the ECU.

We suspect the Ape TM703 dynastart is one of the main sources of electromagnetic interference. The electrical harness was not built using a star ground topology, and the sensor grounds do not run directly from the ECU connector. The ECU case is 3D-printed, lacking metallic shielding against EM pulses. Furthermore, the speed sensor cable—the single most critical signal—runs a long path with small-gauge, unshielded wires. Lastly, the IDE-style connector proved to be extremely sensitive to parasitic signals.

To permanently resolve these issues ahead of future outings, we have planned a series of targeted interventions:

First, we will suppress interference from the dynastart by connecting a 1 µF - 450V capacitor between its ground and positive terminals. To eliminate voltage spikes generated when releasing the starter solenoid, we will insert two 1N4007 diodes in parallel across the control coil pins. We will also add a DC-DC converter (8V-40V to 12V) to guarantee perfectly stable power to the ECU, preventing resets even during voltage drops under cranking load.

We will completely rebuild the electrical system adopting a star layout, separating actuator grounds from sensor grounds, with all of them converging directly onto the ECU connector. For the speed sensor, we will use a shielded cable with the braid grounded on the ECU side, shortening the path and routing it away from electromagnetic radiation sources.

Finally, we will solder the ECU board from scratch: we will use an automotive-grade connector soldered directly onto the PCB with proper wire gauges, all enclosed in a new two-layer box equipped with a grounded copper shield to create a true Faraday cage against external interference.

If you are interested in updates, you can follow the project on [bastardpuller.it](https://www.google.com/search?q=https://www.bastardpuller.it/), [YouTube](https://www.google.com/search?q=https://www.youtube.com/%40bastardpuller), or [Instagram](https://www.google.com/search?q=https://www.instagram.com/bastardpuller/).