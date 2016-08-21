################ Copyright 2005-2016 Team GoldenEye: Source #################
#
# This file is part of GoldenEye: Source's Python Library.
#
# GoldenEye: Source's Python Library is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or(at your option) any later version.
#
# GoldenEye: Source's Python Library is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GoldenEye: Source's Python Library.
# If not, see <http://www.gnu.org/licenses/>.
#############################################################################
import GEUtil, GEMPGameRules
from GEGlobal import EventHooks

def EndMatchCallback( timer, type_ ):
    if type_ == Timer.UPDATE_FINISH:
        GEMPGameRules.EndMatch()

def EndRoundCallback( timer, type_ ):
    if type_ == Timer.UPDATE_FINISH:
        GEMPGameRules.EndRound()

class TimerTracker:
    def __init__( self, parent ):
        if not hasattr( parent, 'RegisterEventHook' ):
            raise AttributeError( "Parent must be a Gameplay Scenario type!" )

        self.timers = []
        self.is_first_run = True
        self.time_last_age = 0
        self._oneshots = 0

        # Register finishCallback to age timers automatically
        parent.RegisterEventHook( EventHooks.GP_THINK, self._age_timers )

    def CreateTimer( self, name ):
        t = Timer( name )
        self.timers.append( t )
        return t

    def RemoveTimer( self, name=None ):
        if not name:
            self.timers = []
        else:
            for t in self.timers:
                if t.GetName() == name:
                    self.timers.remove( t )
                    return

    def OneShotTimer( self, time, callback, update_inter=0.5 ):
        t = Timer( "_oneshot_timer_%d" % self._oneshots )
        t.SetUpdateCallback( callback, update_inter )
        t.Start( time, False )
        self.timers.append( t )
        self._oneshots += 1

    def ResetTimer( self, name=None ):
        for t in self.timers:
            if not name or t.name == name:
                t.Stop()

    def _age_timers( self ):
        now = GEUtil.GetTime()

        if self.is_first_run:
            self.time_last_age = now
            self.is_first_run = False

        delta = now - self.time_last_age
        for t in self.timers:
            t._age_timer( now, delta )
            if t.debug:
                GEUtil.Msg( "[GETimer] Timer %s is %0.1f / %0.1f\n" % ( t.GetName(), t.GetCurrentTime(), t.GetMaxTime() ) )

        self.time_last_age = now

class Timer:
    """
    Simple timer that is registered to a TimerTracker
    This class should not be instantiated outside of a TimerTracker
    """

    ( UPDATE_START, UPDATE_RUN, UPDATE_PAUSE, UPDATE_STOP, UPDATE_FINISH ) = range( 5 )
    ( STATE_RUN, STATE_PAUSE, STATE_STOP ) = range( 3 )

    def __init__( self, name ):
        self.name = name
        # Controls time and trigger points
        self.time_curr = 0
        self.time_max = 0
        self.time_start_aging = 0
        self.time_next_update = 0
        # Control aging of this timer
        self.aging_delay = 0
        self.aging_rate = 0
        # State and flags
        self.state = Timer.STATE_STOP
        self.repeat = False
        # Control update of this timer
        self.update_cb = None
        self.update_rate = 0.25
        self.update_dirty = False
        # For debugging use only
        self.debug = False

    def SetUpdateCallback( self, cb, interval=0.25 ):
        """
        Set an update callback that receives update messages

        Arguments:
            cb -- Callback function, signature must match "def Callback( timer, type_ )"
            interval -- minimum rate that a Timer.UPDATE_RUN will be issued (default 0.25)
        """
        self.update_cb = cb
        self.update_rate = interval
        self.time_next_update = 0

    def SetAgeRate( self, rate, delay=0 ):
        self.aging_rate = rate
        self.aging_delay = delay

    def Start( self, time_max=0, repeat=False ):
        if self.state is Timer.STATE_STOP:
            self.time_curr = 0
            self.time_next_update = 0
            self.time_max = time_max
            self.repeat = repeat

        self.state = Timer.STATE_RUN
        self._call_update( Timer.UPDATE_START )

    def Restart( self ):
        self._call_update( Timer.UPDATE_FINISH )
        self.time_curr = 0
        self.time_next_update = 0
        self.state = Timer.STATE_RUN
        self._call_update( Timer.UPDATE_START )

    def Pause( self ):
        if self.state is Timer.STATE_RUN:
            self.time_start_aging = GEUtil.GetTime() + self.aging_delay
            self.state = Timer.STATE_PAUSE
            self._call_update( Timer.UPDATE_PAUSE )

    def Stop( self ):
        self.repeat = False
        self.state = Timer.STATE_STOP
        self._call_update( Timer.UPDATE_STOP )

    def Finish( self ):
        self._call_update( Timer.UPDATE_FINISH )
        self.Stop()

    def GetName( self ):
        return self.name

    def GetCurrentTime( self ):
        return self.time_curr

    def GetMaxTime( self ):
        return self.time_max

    def _age_timer( self, now, delta ):
        if self.state == Timer.STATE_RUN:
            self.time_curr += delta

            # Check if we are done
            if self.time_max > 0 and self.time_curr >= self.time_max:
                # Repeat if desired, otherwise stop
                if self.repeat:
                    self.Restart()
                else:
                    self.Finish()
            else:
                self.update_dirty = True

        elif self.state == Timer.STATE_PAUSE and self.time_curr > 0:
            # Age the timer if we have it defined
            if now >= self.time_start_aging and self.aging_rate > 0:
                self.time_curr -= delta * self.aging_rate;

                if self.time_curr <= 0:
                    self.time_curr = 0
                    self.Stop()
                else:
                    self.update_dirty = True

        # Attempt an update call
        self._call_update( Timer.UPDATE_RUN )

    def _call_update( self, type_ ):
        now = GEUtil.GetTime()
        # We only attempt this if we have a callback, are a special update or are dirty and its time
        if self.update_cb and ( type_ != Timer.UPDATE_RUN or ( self.update_dirty and now >= self.time_next_update ) ):
            self.time_next_update = now + self.update_rate
            self.update_dirty = False
            # Call into our callback
            self.update_cb( self, type_ )
