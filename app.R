library(billboarder)
library(reticulate)
library(shiny)

source("make_pdf.R")

dsa4w = import("dsa4weather.dsa4weather")

#_Setup_________________________________________________________________________

forecast_length = 30
plot_height = "200px"
icon_size = 50
small_icon_size = "15px"
col_width = 3
row_height = 1
days_per_row = 4
bb_ypad = 500

#_Dependent_constants___________________________________________________________

n_rows = ceiling(forecast_length / days_per_row)

#_Utilities_____________________________________________________________________



tick_format_function = function(values) {
  func_text = "function(value) { const values = ["
  n_values = length(values)
  i = 1
  for (value in values) {
    func_text = paste0(func_text, sprintf("'%s'", value))
    if (i < n_values) {
      func_text = paste0(func_text, ",")
    }
    i = i + 1
  }
  func_text = paste0(func_text, "]; return ' ' + values[value];}")
  return(JS(func_text))
}

make_forecast_symbol = function(forecast, day) {
  icon_name = find_icon_for_weather(forecast, day)
  list(
       src = file.path("icons", icon_name),
       contentType = "image/png",
       width = icon_size,
       height = icon_size
  )
}

forecast_symbol_layout = function(day) {
  column(col_width, 
         h5(paste("Tag", day)),
         # Weather icon_________________________________________________________
         imageOutput(paste0("day", day), 
                     height=sprintf("%spx", icon_size)
         ),
         # Tmax______________________________________________________________
         fluidRow(
           column(1, img(src = file.path("icons", "clouds0.png"), 
                         width = small_icon_size, 
                         height = small_icon_size)),
#           column(1, img(src = "clouds0.png")),
           column(4, textOutput(paste0("Tmax", day)))
         ),
         # Tmin______________________________________________________________
         fluidRow(
           column(1, img(src = file.path("icons", "clouds0_night.png"), 
                         width = small_icon_size, 
                         height = small_icon_size)),
#           column(1, img(src = "clouds0.png")),
           column(4, textOutput(paste0("Tmin", day)))
         ),
         # Wind______________________________________________________________
         imageOutput(paste0("wind", day), 
                     height=sprintf("%spx", icon_size)
         ),
         br()
  )
}

print(tick_format_function(c("a", "b", "c")))


#_UI____________________________________________________________________________

ui = pageWithSidebar(
  headerPanel("DSA 4 Wettergenerator"),
  sidebarPanel(
    selectInput("region", "Region", dsa4w$REGIONS),
    selectInput("season", "Jahreszeit", dsa4w$SEASONS),
    downloadButton("download", "Download pdf"),
    width = 2
  ),
  mainPanel(tabsetPanel(
#_______________________________________________________________________________
    tabPanel(
      "Monatsprognose",
      mainPanel(
        lapply(1:n_rows, function(row) {
          first_day = (row-1) * days_per_row + 1
          last_day = min(forecast_length, row * days_per_row)
          days = first_day:last_day
          fluidRow(lapply(days, forecast_symbol_layout))
        }
        ),
        width = 12
      )
    ),
#_______________________________________________________________________________
    tabPanel(
      "Parameterverläufe",
      billboarderOutput(outputId = "temperature", height = plot_height),
      billboarderOutput(outputId = "precipitation", height = plot_height),
      billboarderOutput(outputId = "wind", height = plot_height),
      billboarderOutput(outputId = "cloudiness", height = plot_height)
    )
  ))
)

#_Server________________________________________________________________________

server = function(input, output, session) {

  weather_generator = reactive({
    dsa4w$DSA4Weather(season = input$season,
                      region = input$region
    )
  })

  forecast = reactive({
    forecast_list = list()
    for (i in 1:forecast_length) {
      wg = weather_generator()
      wg$roll_next_weather()
      tmp = list()
      tmp[["temperature"]] = wg$temperature
      tmp[["night_temperature"]] = wg$night_temperature
      tmp[["cloudiness"]] = wg$cloudiness
      tmp[["wind"]] = wg$wind
      tmp[["precipitation"]] = wg$precipitation
      forecast_list[[i]] = tmp
    }

    # Reformat data
    days = 1:forecast_length
    forecast = data.frame(
      day = days,
      temperature = sapply(days, function(day) {
                             forecast_list[[day]][["temperature"]]
      }),
      night_temperature = sapply(days, function(day) {
                             forecast_list[[day]][["night_temperature"]]
      }),
      wind = sapply(days, function(day) {
                             forecast_list[[day]][["wind"]]
      }),
      cloudiness = sapply(days, function(day) {
                             forecast_list[[day]][["cloudiness"]]
      }),
      precipitation = sapply(days, function(day) {
                             forecast_list[[day]][["precipitation"]]
      })
    ) 
    return(forecast)
  })

  output$temperature = renderBillboarder({
    bb = billboarder()
    bb = bb_linechart(bb, data = forecast(),
                      mapping = bbaes(day, temperature))
    bb = bb_linechart(bb, data = forecast(),
                      mapping = bbaes(day, night_temperature))
    bb = bb %>%
      bb_color(c("red", "blue")) %>%
      bb_labs(y = "Temperatur (Grad Celsius)") %>%
      bb_tooltip(linked = list(name = "day"))
    return(bb)
  })

  output$precipitation = renderBillboarder({
    bb = billboarder()
    bb = bb_linechart(bb, data = forecast(),
                      mapping = bbaes(day, precipitation))
    bb = bb %>%
      bb_color(c("blue")) %>%
      bb_labs(y = "Niederschlagsmenge") %>%
      bb_axis(y = list(tick = list(values = dsa4w$precipitation_levels,
                                   format = tick_format_function(dsa4w$precipitation_strings)
                              )
                  )
      ) %>%
      bb_tooltip(linked = list(name = "day"))
    return(bb)
  })

  output$wind = renderBillboarder({
    bb = billboarder()
    bb = bb_linechart(bb, data = forecast(),
                      mapping = bbaes(day, wind))
    bb = bb %>%
      bb_color(c("blue")) %>%
      bb_labs(y = "Windstärke") %>%
      bb_axis(y = list(tick = list(values = dsa4w$wind_levels,
                                   format = tick_format_function(dsa4w$wind_strings)
                              )
                  )
      ) %>%
      bb_tooltip(linked = list(name = "day"))
    return(bb)
  })

  output$cloudiness = renderBillboarder({
    bb = billboarder()
    bb = bb_linechart(bb, data = forecast(),
                      mapping = bbaes(day, cloudiness))
    bb = bb %>%
      bb_color(c("gray")) %>%
      bb_labs(y = "Bewölkung") %>%
      bb_axis(y = list(tick = list(values = dsa4w$cloud_levels,
                                   format = tick_format_function(dsa4w$cloud_strings)
                              )
                  )
      ) %>%
      bb_tooltip(linked = list(name = "day"))
    return(bb)
  })

  output$sun = renderImage({
      list(
        src = file.path("icons", "clouds0.png"),
        contentType = "image/png",
        width = 50,
        height = 50
      )}, 
    deleteFile = FALSE)

  #_Weather_icons_______________________________________________________________
  lapply(1:forecast_length, function(day) {
           outputId = paste0("day", day)
           output[[outputId]] = renderImage(make_forecast_symbol(forecast(), day),
                                            deleteFile = FALSE)
    }
  )

  #_Min_and_Max_temperatures____________________________________________________
  lapply(1:forecast_length, function(day) {
           outputId = paste0("Tmax", day)
           output[[outputId]] = renderText({
             tmax = forecast()$temperature[[day]]
             sprintf("%s °C", tmax)
           })
        }
  )

  lapply(1:forecast_length, function(day) {
           outputId = paste0("Tmin", day)
           output[[outputId]] = renderText({
             tmax = forecast()$night_temperature[[day]]
             sprintf("%s °C", tmax)
           })
        }
  )

  #_Wind_strength_______________________________________________________________
  lapply(1:forecast_length, function(day) {
      outputId = paste0("wind", day)
      output[[outputId]] = renderImage({
        wind = forecast()$wind[[day]]
        icon_name = sprintf("wind%s.png", wind)
        list( 
          src = file.path("icons", icon_name),
          contentType = "image/png",
          width = icon_size,
          height = icon_size
        )},
        deleteFile = FALSE
      )
    }
  )

  output$download = downloadHandler(
    filename = function() {"test.pdf"},
    content = function(con) {
      make_pdf(forecast())
      file.copy("latest_output.pdf", con)
    }
  )

}

#_Run___________________________________________________________________________

app = shinyApp(ui = ui, server = server)
#runApp(app, port=4343)

