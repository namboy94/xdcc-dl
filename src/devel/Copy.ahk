; Copyright 2014-2017 Hermann Krumrey <hermann@krumreyh.com>
;
; This file is part of mirc-download.
;
; mirc-download is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; mirc-download is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with mirc-download.  If not, see <http://www.gnu.org/licenses/>.

;My Autohotkey Script Collection

;Parameters
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%
SetFormat, float, 0.2


{ ;Autohotkey XDCC Downloader Functions

;This Script allows a download chain of XDCC packs via mIRC
;The data for this must be entered in a .txt file prior to running the script

}

{ ;List of global Variables

	;workdir								Contains the working directory
	;xdccfile								The XDCC .txt file
	;xdccline%number%						The line of the XDCC .txt file saved to variables
	;dlspeed								The speed given in the XDCC .txt file in kB/s
	;series%number%							The name of the series consisting of several packs
	;packsize%number%						The size of a series' packs in MB
	;channel%number%						A series' IRC channel
	;packcount%number%						The number of packs in a series
	;pack%number%							Variable containing pack information
	;totalnumberofpacks						Total number of packs parsed
	;totalnumberofseries					Total number of series parsed
	;logname								Name of the log file
	;totaldownloadsize						Total size of all packs combined in MB
	;totaldownloadsizekb					Total size of all packs combined in KB
	;totaldownloadsizegb					Total size of all packs combined in GB
	;medianpacksize							Median pack size in MB
	;medianpacksizekb						Median pack size in KB
	;medianpacksizegb						Median pack size in GB
	;dltimems								Total Download Size of all packs in ms							
	;dltimeh								Total Download Size of all packs in h
	;dltimemin								Total Download Size of all packs in min
	;dltimes								Total Download Size of all packs in s
	;ircserver%number%						Stores the IRC Server of a Series
}

;Functions

{ ;File Directory Function

	;Should run at the beginning of all scripts and functions that make us of Windows directories
	;defines all Windows directories used in the script for easy editing
	
filedirectoryxdcc(){
	
	global																	;Sets variables in function to global
	
	workdir = %A_ScriptDir%													;Contains the working directory
	configfile = %A_ScriptDir%\config.txt									;links to the config file
	xdccfile = %A_ScriptDir%\input.txt										;The XDCC .txt file
	mirc = %A_ScriptDir%\mIRCportable\mirc.exe								;The mIRC executable
	cmdxexe = %A_ScriptDir%\cmd.exe											;The command prompt executable
	logfiledir = %A_ScriptDir%\logs\										;Directory for log files
	channeldir = %A_ScriptDir%\serverbotlist.txt							;links to the list of irc bots, channels and servers
	
	loop, read, %configfile% 												;File Read Loop
	{					
		IfInString, A_LoopReadLine, ###										;Ignores comments
		{
		local ignore = 1
		}
		IfInString, A_LoopReadLine, default									;Ignores default values
		{
		local ignore = 1
		}
		
		if(ignore = 0){
			
			IfInString, A_LoopReadLine, dir									;Enables directory changes
			{
				IfInString, A_LoopReadLine, inputfiledirectory
				{
					local tempout := A_LoopReadLine
					stringtrimleft, xdccfile, tempout, 23
				}
				IfInString, A_LoopReadLine, logfiledirectory
				{
					local tempout := A_LoopReadLine
					stringtrimleft, logfiledir, tempout, 21
				}
				IfInString, A_LoopReadLine, mIRCdirectory
				{
					local tempout := A_LoopReadLine
					stringtrimleft, mirc, tempout, 18
				}
				IfInString, A_LoopReadLine, cmddirectory
				{
					local tempout := A_LoopReadLine
					stringtrimleft, cmdxexe, tempout, 17
				}
				IfInString, A_LoopReadLine, serverbotlistdirectory
				{
					local tempout := A_LoopReadLine
					stringtrimleft, channeldir, tempout, 27
				}
			}
		}
		
		ignore = 0
		
	}
}
}
{ ;Error Checker

	;Checks if all needed files are present.
	;If not, a notepad file will be opened, which lists the necessary files and terminates the script

errorchecker(){

	global										;Sets variables to global due to compatibility issues

	IfNotExist, %xdccfile%						;If the XDCC file is not in the specified directory, this will terminate the script
	{
		msgBox, %xdccfile% not found.`nPlease put the input file in the specified directory or change the config.txt
		return
	}
	ifNotExist, %mirc%							;If the mIRC executable is not installed in the specified directory, this will terminate the script
	{
		msgBox, %mirc% not found.`nPlease install mIRC in the specfied directory or change the AHK source code
		return
	}
	ifNotExist, %configfile%					;If the config file is not able to be found in the specified directory, this will terminate the script
	{
		msgBox, %configfile% not found.`nPlease put the config.txt file in the same folder as the script
		return
	}
	ifNotExist, %cmdxexe%						;If the CMD executable is not installed in the specified directory, this will terminate the script
	{
		msgBox, %cmdxexe% not found.`nPlease make sure that the path to the cmd file is specified correctly in the config.txt file
		return
	}
	ifNotExist, %logfiledir%					;If the log file folder path is not found, no logs will be created.
	{
		msgBox, %logfiledir% not found.`nNo logs will be created
		nologs = 1
	}
	ifNotExist, %channeldir%					;If the channel data file is not found, the program will be terminated.
	{
		msgBox, %channeldir% not found.`nPlease put the config.txt file in the same folder as the script
		nologs = 1
	}
}
}
{ ;.txt file reader

	;Reads a .txt file and saves the line's contents to variables xdccline%number%

txtfilereader(){
	
	global										;Sets variables in function to global

	local txtline = 1							;local variable txtline for saving the .txt lines in different variables
	
	loop, read, %xdccfile% 						;File Read Loop
	{					
		xdccline%txtline% := A_LoopReadLine		;Saves line to variable xdccline%number%
		txtline++								;Increases txtfile variable by 1
	}
}
}
{ ;Channel Parser
channelparser(){

	global													;Sets variables to global
	servercount = 0										;amount of servers as variable
	
	loop, read, %channeldir% 								;File Read Loop
	{					
		IfInString, A_LoopReadLine, -server					;Starts the saving of channels
		{
			local temvar1 := A_LoopReadLine
			stringtrimleft, temvar2, temvar1, 8
			server%servercount% := temvar2																	;The server variable

			server%servercount%channelcount = 0																	;The amount of channels in a server
			
			local servercounter = -1
			
			loop, read, %channeldir%
			{
				if(servercount = servercounter){
					IfInString, A_LoopReadLine, --channel
					{
						temvar1 := A_LoopReadLine
						stringtrimleft, temvar2, temvar1, 10
						
						local tempochan := server%servercount%channelcount
						server%servercount%channelcount++
						
						server%servercount%channel%tempochan% := temvar2										;The channel variable
						
						server%servercount%channel%tempochan%botcount = 0										;The amount of bots in a channel
						
						local channelcount = -1
						local secondservercounter = -1
						
						loop, read, %channeldir%
						{
							if(channelcount = tempochan) {
								IfInString, A_LoopReadLine, ---packlistbot
								{
									temvar1 := A_LoopReadLine
									stringtrimleft, temvar2, temvar1, 15
									
									local tempobot := server%servercount%channel%tempochan%botcount
									server%servercount%channel%tempochan%botcount++
									server%servercount%channel%tempochan%bot%tempobot% := temvar2
									
								}
							}
							
							if(secondservercounter = servercount){
								IfInString, A_LoopReadLine, --channel
								{
									channelcount++
								}
							}
							
							IfInString, A_LoopReadLine, -server
							{
								secondservercounter++
							}	
						}	
					}
				}
				
				IfInString, A_LoopReadLine, -server
				{
					servercounter++
				}
				
			}
			servercount++
		}
	}
	

}
}
{ ;Channel Checker
channelchecker(packinfo,seriesno){

	global													;Sets variables to global
	
	local servercheck = 0
	local channelcheck = 0
	local botcheck = 0
	
	loop %servercount% {
		
		local serverstring := server%servercheck%
		local channellooper := server%servercheck%channelcount
		loop %channellooper%{
			local channelstring := server%servercheck%channel%channelcheck%
			local botlooper := server%servercheck%channel%channelcheck%botcount
			loop %botlooper%{
				local packstring := server%servercheck%channel%channelcheck%bot%botcheck%
				IfInString, packinfo, %packstring%
				{
				channel%seriesno% = %channelstring%
				ircserver%seriesno% = %serverstring%
				}
				botcheck++
			}
			channelcheck++
			botcheck = 0
		}
		servercheck++
		channelcheck = 0
	}
	
	
	

}
}
{ ;.txt file parser

	;Parses the .txt file and creates multiple variables needed later on.

txtfileparser(){

	global													;Sets variables in function to global
	
	local packnumber = 0									;Sets local variable that keeps track of the pack number
	local seriesnumber = 0									;Sets local variable that keeps track of the series number
	local episodecount = 0									;Sets local variable that keeps track of amount of packs in a series
	local parseline = 4										;Sets local variable that keeps track of the lines of the orginal .txt file
	
	stringtrimleft, dlspeed, xdccline1, 22					;Saves the download speed given in the .txt file (kB/s) to global variable dlspeed
	
	loop{													;parsing loop
		local linecontent := xdccline%parseline%			;saves the current line's content to a useable variable
		if(linecontent = "break"){							;"Break" Event
			seriesnumber++									;Increases variable seriesnumber by 1
			parseline--										;Decreases parseline by 1 to access last pack data
			local channelcheck := xdccline%parseline%		;Saves last pack data to useable local variable
			channelchecker(channelcheck,seriesnumber)		;Determines the channel of the series
			parseline++										;Returns to previous line
			parseline++										;Moves down a line in the original .txt file
			series%seriesnumber% := xdccline%parseline%		;Saves the name of the series in variable series%number%
			parseline++										;Moves down a line in the original .txt file
			local pretrim := xdccline%parseline%			;The size of the packs, but with unnecessary text included
			local posttrim = ""								;Initializes local variable posttrim
			stringtrimleft, posttrim, pretrim, 6			;The size of the current series' packs in MB without unnecessary text
			packsize%seriesnumber% := posttrim				;The size of the current series' packs in MB saved to global variable packsize%number%
			packcount%seriesnumber% := episodecount			;The amount of packs in this series saved to global variable packcount%number%
			episodecount = 0								;resets local variable episodecount for next series 
			parseline++										;Moves down a line in the original .txt file
			parseline++										;Moves down a line in the original .txt file
			parseline++										;Moves down a line in the original .txt file
		}
		else if(linecontent = "stop"){						;"Stop" Event
			break											;Ends the parsing loop
		}
		else if(linecontent = "-"){							;In case of "Airing" Placeholder
			parseline++										;Moves down the txt file to break of "Airing Section"
		}
		else if((linecontent = "..")||(linecontent = "...")||(linecontent = "....")||(linecontent = ".....")||(linecontent = "......")){						
															;Automatically adds systematic packs (e.g pack 1...pack20 will add all packs from 1 to 20) Amount of dots signifies amount of numbers in a pack number(usually 3 or 4)
			parseline--										;Goes up a line
			local continuous1 =								;Stores upper line in local variable
			local continuous2 =								;Stores lower line in local variable
			local starter =									;Stores upper packnumber
			local ender =									;Stores lower packnumber
			local contloop =								;Stores the loop variable locally
			local pattern =									;Saves standard pack pattern
			continuous1 := xdccline%parseline%
			parseline++
			parseline++
			continuous2 := xdccline%parseline%
			stringlen, contlen, continuous1					;Measures Stringlength of single pack
			local cutter =									;Variable to store the amount of unneccesary characters in string
			if(linecontent = ".."){							;Calculates the amount of numbers for the pack and also the standard packet structure
				cutter := contlen-2
				stringtrimright, pattern, continuous1, 2
			}
			else if(linecontent = "..."){
				cutter := contlen-3
				stringtrimright, pattern, continuous1, 3
			}
			else if(linecontent = "...."){
				cutter := contlen-4
				stringtrimright, pattern, continuous1, 4
			}
			else if(linecontent = "....."){
				cutter := contlen-5
				stringtrimright, pattern, continuous1, 5
			}
			else if(linecontent = "......"){
				cutter := contlen-6
				stringtrimright, pattern, continuous1, 6
			}
			stringtrimleft, starter, continuous1, %cutter%
			stringtrimleft, ender, continuous2, %cutter%
			contloop := ender-starter
			starter++
			loop %contloop%{
				packnumber++
				local prelimpack =
				prelimpack = %pattern%%starter%
				starter++
				pack%packnumber% := prelimpack
				episodecount++
			}
			parseline++
		}
		else if((linecontent = ",,")||(linecontent = ",,,")||(linecontent = ",,,,")||(linecontent = ",,,,,")||(linecontent = ",,,,,,")){						
															;Automatically adds systematic packs (e.g pack 1...pack20 will add all packs from 1 to 20) Amount of dots signifies amount of numbers in a pack number(usually 3 or 4)
			parseline--										;Goes up a line
			local continuous1 =								;Stores upper line in local variable
			local continuous2 =								;Stores lower line in local variable
			local starter =									;Stores upper packnumber
			local ender =									;Stores lower packnumber
			local contloop =								;Stores the loop variable locally
			local pattern =									;Saves standard pack pattern
			continuous1 := xdccline%parseline%
			parseline++
			parseline++
			continuous2 := xdccline%parseline%
			stringlen, contlen, continuous1					;Measures Stringlength of single pack
			local cutter =									;Variable to store the amount of unneccesary characters in string
			if(linecontent = ",,"){							;Calculates the amount of numbers for the pack and also the standard packet structure
				cutter := contlen-2
				stringtrimright, pattern, continuous1, 2
			}
			else if(linecontent = ",,,"){
				cutter := contlen-3
				stringtrimright, pattern, continuous1, 3
			}
			else if(linecontent = ",,,,"){
				cutter := contlen-4
				stringtrimright, pattern, continuous1, 4
			}
			else if(linecontent = ",,,,,"){
				cutter := contlen-5
				stringtrimright, pattern, continuous1, 5
			}
			else if(linecontent = ",,,,,,"){
				cutter := contlen-6
				stringtrimright, pattern, continuous1, 6
			}
			stringtrimleft, starter, continuous1, %cutter%
			stringtrimleft, ender, continuous2, %cutter%
			contloop := ender-starter
			starter++
			starter++
			loop %contloop%{
				packnumber++
				local prelimpack =
				prelimpack = %pattern%%starter%
				starter++
				starter++
				pack%packnumber% := prelimpack
				episodecount++
			}
			parseline++
		}
		else{												;Saves packs to variables
			packnumber++									;Increases local variable packnumber by 1
			pack%packnumber% := linecontent					;saves line content to global variable pack%number%
			parseline++										;Moves down a line in the original .txt file
			episodecount++									;Adds a pack to current series' episode counter
		}
	}
	totalnumberofpacks := packnumber
	totalnumberofseries := seriesnumber
}
}
{ ;Statistics calculator

	;Calculates various statstics for use in the log file and/or further calculations
	
statcalc(){

	global																			;Sets variables to global
		
	totaldownloadsize = 0															;intializes global variable to store entire download size in MB
	local seriestotaldownloadsize = ""												;initializes local calculation variable										
	local seriesize = ""															;initializes local calculation variable
	local seriesamount = ""															;initializes local calculation variable
	local seriescounter = 1															;initializes local variable to access global variables
	loop %totalnumberofseries%{														;total download size calculation loop
		seriesamount := packcount%seriescounter%									
		seriesize := packsize%seriescounter%
		seriestotaldownloadsize := seriesamount*seriesize
		totaldownloadsize := totaldownloadsize + seriestotaldownloadsize
		seriescounter++																;increments seriescounter
	}
	medianpacksize := totaldownloadsize/totalnumberofpacks							;global variable that stores themediandownload size of the packs in MB
	medianpacksizekb := medianpacksize*1000											;global variable that stores themediandownload size of the packs in KB
	medianpacksizeGB := medianpacksize/1000											;global variable that stores themediandownload size of the packs in GB
	totaldownloadsizekB := totaldownloadsize*1000									;global variable that saves the total download size in KB
	totaldownloadsizeGB := totaldownloadsize/1000									;global variable that saves the total download size in GB
	dltimes := totaldownloadsizekB/dlspeed											;global variable that save the total download time in s
	dltimemin := dltimes/60															;global variable that save the total download time in min
	dltimeh := dltimes/60/60														;global variable that save the total download time in h
	dltimems := dltimes*1000														;global variable that save the total download time in ms
}
}
{ ;Log File Writer

	;Writes a log to a .txt file in the working directory (workdir).
	;The file name contains the current date and time
	
logfilewriter(){

	global																;Sets variables in function to global
	
	if(nologs = 1) {
	}
	else {
	
	local packlog = 1													;Initalizes local variable packlog to count the packs
	local serieslog = 1													;Initalizes local variable serieslog to count the series
	
	local datevar := A_Now												;sets local variable datevar to current date and time
	logname = %logfiledir%XDCC LOG - %datevar%.txt						;sets global variable logname with the name XDCC LOG - Date&Time.txt
	
	fileappend, XDCC Download Log - %A_NOW%`n`n, %logname%				;Writes the log file to XDCC Log - Date&Time.txt
	fileappend, The following packs were entered:`n`n`n, %logname%
	loop %totalnumberofseries%{											;Log Writing loop for series and packs
		local showname := series%serieslog%								;inputs series name into useable local variable
		local showchannel := channel%serieslog%							;inputs series channel into useable local variable
		local showsize := packsize%serieslog%							;inputs series pack size into useable local variable
		fileappend, Series: `t%showname%`n, %logname%					;enters the series info to the txt file
		fileappend, IRC Channel: `t#%showchannel%`n, %logname%
		fileappend, Pack Size: `t%showsize% MB`n`n, %logname%					
		local numberofeps := packcount%serieslog%						;inputs series' number of packs into useable local variable
		loop %numberofeps%{
			local packet := pack%packlog%								;inputs pack data into useable local variable
			if(packlog<10){												;Variable Tabs If/Else for inputting pack names into txt file
				fileappend, Pack %packlog%:`t`t%packet%`n, %logname%
			}
			else{
				fileappend, Pack %packlog%:`t%packet%`n, %logname%
			}
			packlog++													;Increases packlog by 1
		}
		fileappend, `n`n, %logname%
		serieslog++														;Increases serieslog by 1
	}
	fileappend, `n, %logname%
	fileappend, Download Speed:`t`t`t`t%dlspeed% KB/s`n, %logname%		;Adds statistics to log file
	fileappend, Median Pack Size:`t`t`t%medianpacksizekb% KB`n, %logname%
	fileappend, `t`t`t`t`t%medianpacksize% MB`n, %logname%
	fileappend, `t`t`t`t`t%medianpacksizegb% GB`n, %logname%
	fileappend, Total Download Size:`t`t`t%totaldownloadsizekb% KB`n, %logname%
	fileappend, `t`t`t`t`t%totaldownloadsize% MB`n, %logname%
	fileappend, `t`t`t`t`t%totaldownloadsizegb% GB`n, %logname%
	fileappend, Total Amount of packs:`t`t`t%totalnumberofpacks%`n, %logname%
	fileappend, Total Amount of series:`t`t`t%totalnumberofseries%`n, %logname%
	fileappend, Approximate total download time:`t%dltimems% ms`n, %logname%
	fileappend, `t`t`t`t`t%dltimes% s`n, %logname%
	fileappend, `t`t`t`t`t%dltimemin% min`n, %logname%
	fileappend, `t`t`t`t`t%dltimeh% h, %logname%
	}
}
}
{ ;mIRC Preparer

	;Prepares mIRC for download

mircprepare(){

	global							;sets variables to global
	
	run %mirc%						;starts mIRC
	winwaitactive, mIRC				;waits until mIRC is active
}
}
{ ;mIRC Downloader

	;Downloads from mIRC using previous values

mircdownload(){

	global														;sets variables to global
	
	local mircseries = 1										;local variable for use in the download loop
	local mircpack = 1											;local variable for use in the download loop
	loop %totalnumberofseries%{									;download loop
		local mircchannel = channel%mircseries%					;sets channel as a useable local variable
		local mircserver = ircserver%mircseries%				;sets server as a useable local variable
		send {raw}/server %mircserver%
		send {enter}
		sleep 8000
		local mircsize = packsize%mircseries%					;sets individual packsize as a useable local variable
		local mirctime = ((mircsize*1000)/dlspeed)*1000			;calculates the required download time per pack as a useable local variable
		local mircpackloop = packcount%mircseries%				;repeats loop as many times as there are packs
		loop %mircpackloop%{									;pack enter loop
			send {raw}/join #									;sends /join #channel and presses enter to join channel
			send {raw}%mircchannel%
			send {enter}							
			sleep 1000											;sleeps 1s
			send {esc}											;minimizes channel windows
			sleep 500											;sleeps 0.5s
			local mircpacket := pack%mircpack%					;creates useable local variable to store pack data in
			send {raw}%mircpacket%								;sends pack data and requests it
			sleep 100
			send {enter}
			sleep %mirctime%									;sleeps for the required download time
			mircpack++											;increments mircpack
		}
		mircseries++											;increments mircseries
	}
}
}
{ ;One click downloader

	;Compilation of functions to execute a simple download from input.txt

oneclickdownlog(){

	errorchecker()
	channelparser()
	txtfilereader()
	txtfileparser()
	statcalc()
	logfilewriter()
	mircprepare()
	mircdownload()

}
}
{ ;logless One click downloader

	;Compilation of functions to execute a simple download from input.txt but doesn't create a log file

oneclickdownnolog(){

	errorchecker()
	channelparser()
	txtfilereader()
	txtfileparser()
	statcalc()
	mircprepare()
	mircdownload()

}
}
{ ;GUI

	;Creates a GUI with the program's basic commands

guiactive(){

	global
	
	local wantlog = 1

	Gui, Show, w260 h600, XDCC
	Gui, Add, Button, w200 h100 x30 y25 gDownload, Download
	Gui, Add, Button, w200 h100 x30 gInputFileOpen, Open Input File
	Gui, Add, Button, w200 h100 x30 gServerConfigFileOpen, Open Server Config File
	Gui, Add, Button, w200 h100 x30 gPackLists, Packlists
	Gui, Add, Button, w200 h100 x30 gOpenMirc, Open mIRC
	
	goto Ending
	
	
	Download:
	if(wantlog = 1){
		oneclickdownlog()
	}
	else{
		oneclickdownnolog()
	}
	goto Ending
	
	
	InputFileOpen:
	Run %xdccfile%
	goto Ending
	
	
	ServerConfigFileOpen:
	Run %channeldir%
	goto Ending
	
	PackLists:
	Gui, 2:Show, w260 h600, Packlists
	Gui, 2:Add, Button, w200 h100 x30 y25 gHorriblesubs, Horriblesubs
	Gui, 2:Add, Button, w200 h100 x30 gIntelHaruhichan, Intel Haruhichan
	Gui, 2:Add, Button, w200 h100 x30 gixIRC, ixIRC
	Gui, 2:Add, Button, w200 h100 x30 gNIBL, NIBL
	Gui, 2:Add, Button, w200 h100 x30 gSunXDCC, SunXDCC
	
	goto Ending2
	
	Horriblesubs:
	Run %workdir%\packlists\Horriblesubs.url
	goto Ending2
	
	IntelHaruhichan:
	Run %workdir%\packlists\Intel Haruhichan.url
	goto Ending2
	
	ixIRC:
	Run %workdir%\packlists\ixIRC.url
	goto Ending2
	
	NIBL:
	Run %workdir%\packlists\Nibl.url
	goto Ending2
	
	SunXDCC:
	Run %workdir%\packlists\Sun XDCC.url
	goto Ending2

	
	Ending2:
	goto Ending
	
	OpenMirc:
	Run %mirc%
	goto Ending
	
	;Websites:
	;goto Ending
	
	;OpemMirc:
	;Run %mirc%
	;Gui, 2:Show, w260 h400, Packlists
	;goto Ending
	
	
	Ending:
	
	return
	
}
}
filedirectoryxdcc()
guiactive()

;TODO Automatic bot adder
;TODO Single Pack Downloader
;TODO Add to input file
;TODO Reset Input File