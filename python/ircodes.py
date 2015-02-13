__author__ = 'gmuralit'


class IRCodes56():
    """
    IRCodes for SA 56 kHz
    """

    def __init__(self):
        self.protocol = '08'
        self.data_size = '2'
        self.key0 = '1b19'
        self.key1 = '1b10'
        self.key2 = '1b11'
        self.key3 = '1b12'
        self.key4 = '1b13'
        self.key5 = '1b14'
        self.key6 = '1b15'
        self.key7 = '1b16'
        self.key8 = '1b17'
        self.key9 = '1b18'
        self.channel_up = '1b1d'
        self.channel_down = '1b1e'
        self.exit = '1b2c'
        self.select = '1b0c'
        self.pwr = '1b07'
        self.info = '1b08'
        


class IRCodesDTA():
    """
    IRCodes for DTA XMP
    """

    def __init__(self):
        self.protocol = '14'
        self.data_size = '8'
        self.key0 = '170f443e1f000000'
        self.key1 = '170f443e1e000100'
        self.key2 = '170f443e1d000200'
        self.key3 = '170f443e1c000300'
        self.key4 = '170f443e1b000400'
        self.key5 = '170f443e1a000500'
        self.key6 = '170f443e19000600'
        self.key7 = '170f443e18000700'
        self.key8 = '170f443e17000800'
        self.key9 = '170f443e16000900'
        self.channel_up = '170f443e12000d00'
        self.channel_down = '170f443e11000e00'
        self.exit = '170f443e13002a00'
        self.pwr = '170f443e10000f00'
        self.select = '170f443e19002400'
        self.enter = '170f443e18002500'
        self.last = '170f443e19005100'
        


class IRCodesMotorola():
    """
    IRCodes for Motorola
    """

    def __init__(self):
        self.data_size      = '2'
        self.protocol       = '15'
        self.arrowUp        = '3490'
        self.arrowLeft      = '3670'
        self.arrowRight     = '3760'
        self.pause          = '1f00'
        self.guide          = '30d0'
        self.pwr            = '0a60'
        self.info           = '33a0'
        self.arrowDown      = '3580'
        self.select         = '11e0' # SELECT/OK
        self.bypass         = '14b0' # INPUT/RF BYPASS
        self.last           = '13c0'
        self.key1           = '01f0'
        self.key2           = '02e0'
        self.key3           = '03d0'
        self.key4           = '04c0'
        self.key5           = '05b0'
        self.key6           = '06a0'
        self.key7           = '0790'
        self.key8           = '0880'
        self.key9           = '0970'
        self.key0           = '0000'
        self.live           = '01f0'
        self.skipAhead      = '3fe0'
        self.channel_up      = '0b50' # Same as pageUp
        self.channel_down    = '0c40' # Same as pageDown
        self.favorite       = '15a0'
        self.volumeUp       = '0d30'
        self.volumeDown     = '0e20'
        self.mute           = '0f10'
        self.list           = '3d00' # DVR
        self.replay         = '3c10'
        self.fastForward    = '1d20'
        self.rewind         = '1e10'
        self.dot            = '4480' # * / CC
        self.pound          = '40c0' # / ASPECT
        self.exit           = '12d0'
        self.A              = '1780' # A (Yellow Triangle)
        self.B              = '2770' # B (Blue Square)
        self.C              = '2860' # C (Red Circle)
        self.play           = '1b40'
        self.stop           = '1c30'
        self.record         = '31c0'
        self.pageUp         = '0b50' # Same as chUp
        self.pageDown       = '0c40' # Same as chDown
        self.settings       = '42a0' # Options
        self.pip            = '22c0'
        self.pipSwap        = '23b0'
        self.menu           = '1960'
