import streamlit as st
import pandas as pd
import geopandas as gpd

# Configure the page
st.set_page_config(
    page_title="Interactive Data Table Viewer",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .column-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .notebook-link {
        background-color: #4bbfff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .notebook-link:hover {
        background-color: #ff6b6b;
        color: white;
        text-decoration: none;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """
    Load your main data table and column descriptions.
    Replace this function with your actual data loading logic.
    """
    # Example data - replace with your actual data loading
    # read data from geojson
    data_path = "https://github.com/FAIRiCUBE/uc1-urban-climate/blob/55742139337e20a1708ab3193ec26295d0a0c5c5/data/city_features_collection/city_features_collection_v0.1.geojson?raw=true"
    codebook_path = "city_features_collection/city_features_collection_codebook.csv"
    main_df = gpd.read_file(data_path)

    # read column descriptions from CSV
    column_descriptions = pd.read_csv(codebook_path)
    print("Column descriptions loaded:", column_descriptions['feature'].tolist())
    print("Main DataFrame columns:", main_df.columns.tolist())
    return main_df, column_descriptions


def main():
    st.title("📊 European Cities Atlas")
    # use the markdown from the readme
    st.markdown(
        """
    This app provides an interactive data table viewer for the European Cities Atlas dataset, 
    a comprehensive dataset providing standardized indicators for approximately 700 European cities, offering a systematic overview of urban characteristics across Europe for the reference year 2018.
    It allows users to explore city features, view column descriptions, and access processing notebooks for each feature.
    
    For more information, click below or visit the [GitHub repository](https://github.com/FAIRiCUBE/uc1-urban-climate).
    """
    )

    # add expandable section for more information
    with st.expander("More Information", expanded=False):
        st.markdown(
            """
## Overview

The European Cities Atlas integrates multiple data sources to create a unified resource for urban research and policy analysis. This dataset enables comparative studies across European cities by providing consistent metrics on physical, environmental, and socioeconomic characteristics.

## Indicators

The dataset encompasses three core thematic areas:

**Land Use & Physical Characteristics**
- Urban fabric density and composition
- Green and blue infrastructure coverage
- Topographical features and elevation data
- Sealed surface percentages and tree cover

**Climate & Environmental Conditions**
- Temperature profiles and thermal comfort indices
- Seasonal weather patterns (summer days, tropical nights)
- Environmental zone classifications
- Coastal proximity indicators

**Socioeconomic Demographics**
- Population structure and age distribution
- Economic activity and employment statistics
- Income levels and health indicators
- Urban development patterns

For detailed specifications of all indicators, refer to the comprehensive codebook `cities_features_collection_codebook.csv`. Categorical feature definitions are provided in accompanying codelists `codelist_<feature>.csv`.

## Geographic Coverage

City boundaries and selection criteria are based on the Eurostat Urban Atlas, ensuring consistency with official European urban statistical frameworks. The dataset covers cities across all EU member states plus additional European countries included in the Urban Audit.

**Source geometries available in multiple coordinate systems:**
- EPSG:4326 (WGS84): <https://gisco-services.ec.europa.eu/distribution/v2/urau/geojson/URAU_RG_01M_2018_4326_CITIES.geojson>
- EPSG:3035 (European grid): <https://gisco-services.ec.europa.eu/distribution/v2/urau/geojson/URAU_RG_01M_2018_3035_CITIES.geojson>

Additional information on the Urban Audit methodology and city selection criteria is available from [Eurostat GISCO](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/urban-audit).

## Metadata

STAC metadata record available on the FAIRiCUBE Data Catalogue: https://catalog.eoxhub.fairicube.eu/collections/index/items/city_features_collection

## Example usage

Clustering analysis of European cities: check out this interactive demo notebook: `notebooks\\demo\\cities_clustering_interactive_demo.ipynb`.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)""")
        
    # Load data
    df, column_descriptions = load_data()

    if df is None or column_descriptions is None:
        st.error("Failed to load data. Please check your files.")
        return

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Data Table")

        # Column selection for display
        columns_to_show = st.multiselect(
            "Select columns to display:",
            options=list(df.columns),
            default=list(df.columns)[:5],  # Show first 5 columns by default
        )

        # Display the filtered table
        if columns_to_show:
            display_df = df[columns_to_show]
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=700,
            )
        else:
            st.warning("Please select at least one column to display.")

    with col2:
        st.header("Column Information")

        # Column selector
        selected_column = st.selectbox(
            "Select a column to view details:", options=list(df.columns), index=0
        )

        print("Selected column:", selected_column)
        print(column_descriptions.columns)
        print(df.columns)
        if selected_column:
            col_info = column_descriptions.loc[
                column_descriptions["feature"] == selected_column
            ].iloc[0]

            # Display column information
            # feature,feature_description,source_dataset,processing,unit,reference_year,data_type,contains_null,remarks
            st.markdown(
                f"""
            <div class="column-info">
                <h4>{selected_column}</h4>
                <p><strong>Name:</strong> {col_info['feature_name']}</p>
                <p><strong>Description:</strong> {col_info['feature_description']}</p>
                <p><strong>Processing method:</strong> {col_info['processing_method']}</p>
                <p><strong>Source dataset:</strong> <a href='{col_info['source_dataset']}' target='_blank'>{col_info['source_dataset']}</a></p>
                <p><strong>Unit:</strong> {col_info['unit']}</p>
                <p><strong>Reference year:</strong> {col_info['reference_year']}</p>
                <p><strong>Data type:</strong> {col_info['data_type']}</p>
                <p><strong>Contains null values:</strong> {col_info['contains_null']}</p>
                <p><strong>Remarks:</strong> {col_info['remarks']}</p>
                <a href="{col_info['notebook_path']}" target="_blank" class="notebook-link">
                    📓 View Processing Notebook on GitHub
                </a>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Basic statistics for the column
            if selected_column in df.columns:
                st.subheader("Column Statistics")
                if df[selected_column].dtype in ["int64", "float64"]:
                    stats = df[selected_column].describe()
                    st.write(stats)
                else:
                    st.write(f"Data type: {df[selected_column].dtype}")
                    st.write(f"Unique values: {df[selected_column].nunique()}")
                    st.write(f"Missing values: {df[selected_column].isnull().sum()}")

        # Data summary
        st.subheader("Dataset Summary")
        st.write(f"**Total rows:** {len(df):,}")
        st.write(f"**Total columns:** {len(df.columns)}")
        st.write(f"**Missing values:** {df.isnull().sum().sum()}")


if __name__ == "__main__":
    main()
