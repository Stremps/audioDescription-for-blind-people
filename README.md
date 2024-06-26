
# Audio Description Project for Visually Impaired

## Overview
This project aims to validate the potential of providing targeted audio descriptions for visually impaired individuals using Head-Mounted Displays (HMDs). Each directory in this repository contains Python scripts designed to communicate with the ChatGPT-4o model, sending images for descriptive analysis and receiving audio outputs tailored to specific needs.

## Algorithm Options

### `AudioDescription`
This directory contains scripts that generate a general description of the scenario based on a screenshot. The audio output provides an overall context of the environment, enhancing spatial awareness for visually impaired users.
<div align="center">
  <img src="https://i.ibb.co/d0Gnbv9/general2-Borrado.jpg" width="30%" height="30%" alt="Example of AudioDescription Base">
</div>

### `AudioDescriptionLocomotion`
Scripts in this directory assist with locomotion by describing the path ahead. They focus on identifying clear pathways and highlighting obstacles, thus aiding users in navigating their environments safely.
<div align="center">
  <img src="https://i.ibb.co/c3SXV7Q/locomotion1-Borrado.jpg" width="30%" height="30%" alt="Example of AudioDescription Locomotion">

### `AudioDescriptionPerson`
The focus of this directory is to describe the facial features of a person centered on the screen. These scripts provide detailed descriptions of facial characteristics, helping users form a mental image of the people around them.
<div align="center">
  <img src="https://i.ibb.co/6rdXdkn/people2-Borrado.jpg" width="30%" height="30%" alt="Example of AudioDescription Person">
</div>

### `AudioDescriptionText`
This directory's scripts are designed to read any text present in front of the user. They help in accessing written content, which can be crucial for independent interaction with various environments.
<div align="center">
  <img src="https://i.ibb.co/hs51hyk/text1-Borrado.jpg" width="30%" height="30%" alt="Example of AudioDescription Text">
</div>

## Project Purpose
The purpose of this project is to explore and demonstrate how specific audio descriptions generated through advanced AI models like ChatGPT-4o can aid visually impaired individuals. By leveraging HMD technology, the project seeks to create more inclusive and accessible experiences, potentially transforming how visually impaired individuals perceive and interact with the world.

## Usage
To use the scripts, follow the setup instructions provided in the directory "audiodescription". Each script is designed to interface seamlessly with ChatGPT-4o for real-time processing of visual data captured through HMDs.
