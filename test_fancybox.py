"""
FancyBox unittests
"""
from pelican import signals

def fancybox_plugin():
    "Fanxybox plugin - temporary code placement"
    pass

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)

def is_receiver_registered(receiver_name):
    'Checks if receiver is registered to signals generator'
    return signals.article_generator_finalized.has_receivers_for(receiver_name)

def test_plugin_registers():
    """
    Check if plugin registers to article_generator_finalized
    """
    register()
    assert is_receiver_registered(fancybox_plugin)
