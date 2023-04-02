from dataclasses import dataclass
import pygame, pytmx, pyscroll


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_map: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: []
    map_layer: False


class MapManager:

    def __init__(self, screen, player, panels=False):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "map"
        self.panels = []

        self.register_map("map", portals=[
            Portal(from_world="map", origin_point="enter_house_1", target_map="house_1", teleport_point="player"),
            Portal(from_world="map", origin_point="enter_house_2", target_map="house_2", teleport_point="player"),
            Portal(from_world="map", origin_point="enter_house_3", target_map="house_3", teleport_point="player")], panels=panels)
        self.register_map("house_1", portals=[
            Portal(from_world="house_1", origin_point="return", target_map="map", teleport_point="player"),
        ])
        self.register_map("house_2", portals=[
            Portal(from_world="house_2", origin_point="return", target_map="map", teleport_point="exit_2"), ])
        self.register_map("house_3", portals=[
            Portal(from_world="house_3", origin_point="return", target_map="map", teleport_point="exit_3"), ])

        self.teleport_player("player")

    def check_collisions(self):
        # potrals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_map
                    self.teleport_player(copy_portal.teleport_point)
        # collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def redraw_map(self, panels=False):
        self.register_map("map", portals=[
            Portal(from_world="map", origin_point="enter_house_1", target_map="house_1", teleport_point="player"),
            Portal(from_world="map", origin_point="enter_house_2", target_map="house_2", teleport_point="player"),
            Portal(from_world="map", origin_point="enter_house_3", target_map="house_3", teleport_point="player")], panels=panels)

    def register_map(self, name, portals=[], panels={}):
        tmx_data = pytmx.util_pygame.load_pygame(f"{name}.tmx")
        if panels:
            tile_gid = tmx_data.get_tile_gid(2, 11, 1)
            print(tmx_data.layers[1].data)
            print('TILE GID :')
            print(tile_gid)
            for panel in panels.values():
                print('PANEL :')
                print(panel)
                x, y = panel
                tmx_data.layers[1].data[int(x//60)][int(y//60)] = tile_gid
        print('GOT NEW MAP, GIVING TO TILED MAP DATA')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'panel':
                self.panels.append({'name': obj.name, 'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height)})

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        # map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, map_layer)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self, nocenter=False):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

    def get_panels(self):
        return self.panels
    
    def add_panel(self, panel):
        if any([panel['name'] == x['name'] for x in self.get_panels()]):
            return
        self.panels.append(panel)
