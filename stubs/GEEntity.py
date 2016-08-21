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
import GEPlayer, GEUtil

def GetUID( ent ):
    '''Get an entity's Unique ID'''
    return int

def GetEntByUniqueId( uid ):
    '''Get an entity by it's Unique ID'''
    return CBaseEntity

def GetEntByUID( uid ):
    '''Get an entity by it's Unique ID'''
    return CBaseEntity

def GetEntitiesInBox( classname, origin, mins, maxs ):
    '''
    Find all the entities of the given classname in the provided box coordinates.

    Arguments:
    classname -- Desired entity classname to search (string)
    origin -- Origin of the search box (GEUtil.Vector)
    mins -- Relative min extents of the search box (GEUtil.Vector)
    maxs -- Relative max extents of the search box (GEUtil.Vector)
    '''
    return []

class EntityHandle:
    '''
    Safe way to store an entity while retaining direct access
    Use by initialization: hEnt = GEEntity.EntityHandle( ent )
    Then retrieve with: hEnt.Get()  <-- Check for None!
    '''

    def __init__(self, ent):
        '''Create a handle to the given entity, this provides safe pointer usage.'''
    
    def Get(self):
        '''
        Get the entity this handle is pointing to. This will return None
        if the referenced entity is no longer valid.
        '''
        return CBaseEntity
    
    def GetUID(self):
        '''Return the Unique ID of the referenced entity.'''
        return int
    
class CBaseEntity:
    '''Representation of a game entity'''

    def GetParent(self):
        return CBaseEntity
    
    def GetPlayerOwner(self):
        return GEPlayer.CBaseCombatCharacter
    
    def GetOwner(self):
        return CBaseEntity
    
    def GetTargetName(self):
        '''Get the map-based target name of the entity'''
        return str
        
    def SetTargetName(self):
        '''Set the map-based target name of the entity'''
        
    def GetClassname(self):
        return str
    
    def SetModel(self, model):
        '''Set the model of this entity with the provided model path'''
        
    def IsAlive(self):
        return bool
    
    def IsPlayer(self):
        return bool
    
    def IsNPC(self):
        return bool
    
    def GetTeamNumber(self):
        return int
    
    def GetAbsOrigin(self):
        return GEUtil.Vector
        
    def SetAbsOrigin(self, origin):
        '''Set this entity's absolute origin (GEUtil.Vector)'''
    
    def GetAbsAngles(self):
        return GEUtil.QAngle
        
    def SetAbsAngles(self, angles):
        '''Set this entity's absolute angles (GEUtil.QAngle)'''
    
    def GetEyeAngles(self):
        return GEUtil.Vector
    
    def GetUID(self):
        return int
    
    def GetIndex(self):
        return int
