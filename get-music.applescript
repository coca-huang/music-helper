on run {args}
	tell application "Music"
		try
			-- get music state
			if player state is not stopped then
				set MusicState to "playing"
			else
				set MusicState to "paused"
			end if
			-- get music name and artist
			set MusicName to name of current track
			set MusicArtist to artist of current track
			-- get music artwork
			tell artwork 1 of current track
				if format is JPEG picture then
					set MusicArtworkType to ".jpg"
				else
					set MusicArtworkType to ".png"
				end if
			end tell
			set MusicArtworkRaw to (get raw data of artwork 1 of current track)
			-- save artwork image
			set ArtworkPath to (args & "artwork" & MusicArtworkType) as text
			try
				tell me to set FileRef to (open for access ArtworkPath with write permission)
				write MusicArtworkRaw to FileRef starting at 0
				tell me to close access FileRef
			on error m number n
				-- display dialog "Image save failed." & m & n & ArtworkPath
				try
					tell me to close access FileRef
				end try
				return
			end try
			-- return as expected
			return {MusicState, MusicName, MusicArtist, MusicArtworkType}
		on error
			-- display dialog "Music is not available."
			return
		end try
	end tell
end run
