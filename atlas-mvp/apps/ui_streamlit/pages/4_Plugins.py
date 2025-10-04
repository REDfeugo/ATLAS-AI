"""Plugin manager page."""

import streamlit as st

from apps.ui_streamlit.utils import state

st.set_page_config(page_title="Plugins", page_icon="🧩")


def main() -> None:
    """List plugins and allow running them with a simple payload."""

    app_state = state.get_app_state()
    st.title("🧩 Plugins")

    st.write(
        """
        Plugins are lightweight Python modules stored in the `plugins/` directory.
        Each plugin defines a `manifest.yaml` describing its name, description, and
        the path to a `run(payload)` function. Enable or disable them here!
        """
    )

    available = app_state.api_client.list_plugins()
    if not available:
        st.warning("No plugins discovered yet. See docs/02_PLUGINS.md to add one.")
        return

    for plugin in available:
        with st.expander(plugin["name"], expanded=False):
            st.write(plugin["description"])
            enabled = st.checkbox(
                "Enabled", value=plugin.get("enabled", False), key=f"plugin_{plugin['name']}"
            )
            app_state.api_client.set_plugin_enabled(plugin["name"], enabled)

            st.markdown("### Run plugin")
            payload = st.text_area(
                "JSON payload", value="{}", help="Provide arguments expected by the plugin"
            )
            if st.button("Execute", key=f"run_{plugin['name']}"):
                result = app_state.api_client.run_plugin(plugin["name"], payload)
                st.write(result)

    st.caption("BEGINNER TIP: Edit `plugins/example_tool` to build your own utilities.")


if __name__ == "__main__":
    main()
