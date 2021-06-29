# Fro: https://gist.github.com/rentzsch/1047967

property inspect : "inspect"
property devTools : "DevTools"

tell application "Chrome"
	set windowList to every tab of every window whose URL contains inspect
	repeat with tabList in windowList
		set tabList to tabList as any
		repeat with tabItr in tabList
			set tabItr to tabItr as any
			delete tabItr
		end repeat
	end repeat
	set windowList to every tab of every window whose URL contains devTools
	repeat with tabList in windowList
		set tabList to tabList as any
		repeat with tabItr in tabList
			set tabItr to tabItr as any
			delete tabItr
		end repeat
	end repeat
end tell
