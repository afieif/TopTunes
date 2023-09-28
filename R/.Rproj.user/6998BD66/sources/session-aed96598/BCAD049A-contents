library(shiny)
library(dplyr)
library(plotly)

# Load data from CSV file
load_data <- function() {
  df <- read.csv('../charts.csv', stringsAsFactors = FALSE)  # Update the path if needed
  return(df)
}

df <- load_data()

# Define UI
ui <- fluidPage(
  sidebarLayout(
    sidebarPanel(
      selectInput("page", "Choose a Page", choices = c("Dashboard", "Artists")),
      conditionalPanel(
        condition = "input.page == 'Dashboard'",
        selectInput("song", "Select Song:", c("All", unique(df$song)))
      ),
      conditionalPanel(
        condition = "input.page == 'Artists'",
        selectInput("year", "Select a Year:", unique(substr(df$date, 1, 4)))
      )
    ),
    mainPanel(
      uiOutput("content")
    )
  )
)

# Define server
server <- function(input, output) {
  output$content <- renderUI({
    if (input$page == "Dashboard") {
      selected_song <- input$song
      
      filtered_data <- df
      if (selected_song != "All") {
        filtered_data <- filtered_data %>%
          filter(song == selected_song)
      }
      
      dashboard_output <- list(
        fluidRow(
          column(12, plotlyOutput("line_chart")),
        ),
        fluidRow(
          column(12, tableOutput("filtered_data_table"))
        )
      )
      
      return(dashboard_output)
    } else if (input$page == "Artists") {
      selected_year <- input$year
      top_artists_by_year <- df %>%
        filter(substr(date, 1, 4) == selected_year)
      top_artists <- top_artists_by_year %>%
        group_by(artist) %>%
        summarize(mean_rank = mean(rank)) %>%
        arrange(mean_rank)
      
      compare_artists_output <- list(
        plotlyOutput("bar_chart")
      )
      
      return(compare_artists_output)
    }
  })
  
  output$line_chart <- renderPlotly({
    # Line Chart
    filtered_data <- df
    if (!is.null(input$song) && input$song != "All") {
      filtered_data <- filtered_data %>%
        filter(song == input$song)
    }
    
    line_chart <- plot_ly(filtered_data, x = ~date, y = ~rank, color = ~song, type = 'scatter', mode = 'lines', text = ~song) %>%
      layout(title = "Rank Over Time")
    
    return(line_chart)
  })
  
  output$filtered_data_table <- renderTable({
    filtered_data <- df
    if (!is.null(input$song) && input$song != "All") {
      filtered_data <- filtered_data %>%
        filter(song == input$song)
    }
    
    return(filtered_data)
  })
  
  output$bar_chart <- renderPlotly({
    # Bar Chart for Compare Artists
    selected_year <- input$year
    top_artists_by_year <- df %>%
      filter(substr(date, 1, 4) == selected_year)
    top_artists <- top_artists_by_year %>%
      group_by(artist) %>%
      summarize(mean_rank = mean(rank)) %>%
      arrange(mean_rank)
    
    bar_chart <- plot_ly(top_artists, x = ~mean_rank, y = ~artist, type = 'bar', orientation = 'h') %>%
      layout(title = paste("Top Artists in", selected_year), height = 700)
    
    return(bar_chart)
  })
}

# Run the Shiny app
shinyApp(ui, server)
