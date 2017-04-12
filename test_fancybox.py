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

def test_plugin_registers():
    """
    Check if plugin registers to article_generator_finalized
    """
    register()
    assert signals.article_generator_finalized.has_receivers_for(fancybox_plugin)
