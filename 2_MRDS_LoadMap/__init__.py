


def classFactory(iface):
    """Load MRDS_Load_Road class from file mrds_load_map."""
    from mrds_load_map import MRDS_Load_Map
    return MRDS_Load_Map(iface)
