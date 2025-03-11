from ...base_chapter import BaseChapter

class VisualNovel(BaseChapter):
    def __init__(self, root, settings, audio_manager):
        chapter_info = {
            "name": "Ato 2",
            "narration_file": "chapters/two/ato2/narration/narracao_ato2.txt",
            "number": 2
        }
        super().__init__(root, settings, audio_manager, chapter_info)
        
        # Start background music
        self.audio.play_music("background.mp3", loop=True)
        
        # Setup auto-save if enabled
        if self.settings.get_setting("auto_save", "enabled"):
            self.setup_auto_save()
