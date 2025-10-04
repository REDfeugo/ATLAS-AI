"""Plugin management page."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.ui_streamlit.components import brand_header, permission_badge
from apps.ui_streamlit.utils import state

PAGE_ICON = str(Path(__file__).resolve().parents[2] / "brand" / "atlas_avatar.svg")

st.set_page_config(page_title="Plugins", page_icon=PAGE_ICON)


def main() -> None:
    """List plugins and allow running them with a simple payload."""

    app_state = state.get_app_state()
    health = app_state.api_client.health_check()

    brand_header.render(
        title="Atlas Plugins",
        subtitle="Extend Atlas carefully with local tools.",
        health_payload=health,
        mode_label="Local-first",
    )

    st.write(
        """
        Plugins are lightweight Python modules stored in the `plugins/` directory.
        Each plugin defines a `manifest.yaml` describing its name, description, and
        the path to a `run(payload)` function. Enable or disable them here!
        """
    )

    available = app_state.api_client.list_plugins()
    if not available:
        st.markdown(
            "<div class='atlas-empty'>No plugins discovered yet. See docs/02_PLUGINS.md to add one.</div>",
            unsafe_allow_html=True,
        )
        return

    for plugin in available:
        with st.expander(plugin["name"], expanded=False):
            st.write(plugin.get("description", "No description provided."))
            col1, col2 = st.columns([1, 2])
            with col1:
                enabled = st.checkbox(
                    "Enabled",
                    value=plugin.get("enabled", False),
                    key=f"plugin_{plugin['name']}",
                )
            with col2:
                tier = plugin.get("permission", "ask")
                st.markdown("**Permission tier**")
                permission_badge.render(tier)
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
