from fastapi import FastAPI
from fastapi.middleware.cors import  CORSMiddleware
import subprocess
import os
import re
import sys
from agent_rebel import ai_manager,ai_worker